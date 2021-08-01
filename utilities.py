import yaml

config = {}

with open('config.yml', 'r') as file:
    try:
        config = yaml.safe_load(file)
        print('config.yml loaded!')
    except yaml.YAMLError as ex:
        print(ex)

token = config['token']
prefix = config['prefix']
dev_channel = config['dev_channel']
dev_id = config['dev_id']
sendgrid_api_key = config['sendgrid_api_key']
code_range = config['code_range']
server_id = config['server_id']
verification_channel = config['verification_channel']
instructions_channel = config['instructions_channel']
officer_role = config['officer_role']
verified_role = config['verified_role']
guest_role = config['guest_role']