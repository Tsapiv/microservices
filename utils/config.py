# import yaml
#
#
# def load_config(filename):
#     with open(filename, 'r') as stream:
#         try:
#             return yaml.safe_load(stream)
#         except yaml.YAMLError as exc:
#             print(exc)

def get_ports(consul):
    res = {'logging': [], 'messages': []}
    for key, value in consul.agent.services().items():
        if key.startswith('logging'):
            res['logging'].append(value['Port'])
        elif key.startswith('messages'):
            res['messages'].append(value['Port'])
    return res