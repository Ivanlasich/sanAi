import yaml

conf_name = 'stress_pod_memory.yml'
with open(conf_name, 'r') as stream:
    try:
        print('{0}Mi'.format(8))
        myyaml = yaml.safe_load(stream)
        #print(myyaml)
        print(myyaml['spec']['containers'][0]['name'])
        myyaml['spec']['containers'][0]['resources']['limits']['cpu'] = '{0}'.format(8)
        print(myyaml['spec']['containers'][0]['resources']['limits']['cpu'])
    except yaml.YAMLError as exc:
        print(exc)
