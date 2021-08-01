import utilities
import random
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Verification(commands.Cog, name = 'Verification'):
    def __init__(self, bot):
        self.bot = bot
        self.codes = {}

    def send_email(self, email, user):
        code = random.randint(1, utilities.code_range)
        message = Mail(
            from_email='unicycleclubosu@gmail.com',
            to_emails=email,
            subject='Unicycle Club at The Ohio State University Discord Verification',
            html_content=f'''<h1>Unicycle Club at The Ohio State University Verification</h1>
            <p>Thank you for your interest in Unicycle Club at The Ohio State University. Your verification code is <strong>{code}</strong></p>
            <p>Type (<strong>DO NOT</strong> copy) the following command in the Discord server to verify yourself:</p>
            <p style="font-family:courier;">/code {code}</p>'''
        )
        try:
            sg = SendGridAPIClient(utilities.sendgrid_api_key)
            response = sg.send(message)
            self.codes[user] = code
        except Exception as e:
            raise e

    @cog_ext.cog_slash(
        name = 'guest',
        description = 'Receive the guest role for non OSU students',
        guild_ids = [utilities.server_id]
    )
    async def _guest(self, ctx: SlashContext):
        if ctx.guild.get_role(utilities.guest_role) in ctx.author.roles:
            await ctx.send('You already have the guest role!', hidden = True)
        else:
            await ctx.author.add_roles(ctx.guild.get_role(utilities.guest_role))
            await ctx.guild.get_channel(utilities.dev_channel).send(f'<@{ctx.author.id}> Has just been given the guest role!')
            await ctx.send('You have been given the guest role and granted access to the server!', hidden = True)

    @cog_ext.cog_slash(
        name = 'verify',
        description = 'Enter your OSU email to get a verification code and gain access to the server',
        guild_ids = [utilities.server_id],
        options = [
            create_option(
                name="email",
                description="Your full OSU email (Ex: brutus.1@osu.edu)",
                option_type=3,
                required=True
            )
        ]
    )
    async def _verify(self, ctx: SlashContext, email: str):
        if ctx.guild.get_role(utilities.verified_role) in ctx.author.roles:
            await ctx.send('You are already verified!', hidden = True)
        else:
            if (email.endswith('osu.edu')):
                self.send_email(email, ctx.author.id)
                await ctx.send(f'An email has been sent to {email}', hidden = True)
            else:
                await ctx.send(f'You must verify with an OSU email. If you think this is a mistake, ping an officer by typing <@&{utilities.officer_role}>', hidden = True)

    @cog_ext.cog_slash(
        name = 'code',
        description = 'Enter the verification code sent to your email after using /verify',
        guild_ids = [utilities.server_id],
        options = [
            create_option(
                name="code",
                description="The verification code sent to your OSU email after using /verify",
                option_type=3,
                required=True
            )
        ]
    )
    async def _code(self, ctx: SlashContext, code: str):
        if ctx.guild.get_role(utilities.verified_role) in ctx.author.roles:
            await ctx.send('You are already verified!', hidden = True)
        else:
            if str(self.codes.get(ctx.author.id)) == str(code):
                await ctx.author.add_roles(ctx.guild.get_role(utilities.verified_role))
                self.codes.pop(ctx.author.id)
                await ctx.guild.get_channel(utilities.dev_channel).send(f'<@{ctx.author.id}> Has just been verified!')
                await ctx.send('You have been successfully verified and granted access to the server!', hidden = True)
            else:
                await ctx.send('Invalid code. Please try again.', hidden = True)

def setup(bot):
    bot.add_cog(Verification(bot))

