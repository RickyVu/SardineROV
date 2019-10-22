# [ModuleName]:
#   - Parameter1: Value
#     Parameter2: Value
#   - Parameter1: Value
#     Parameter2: Value



 # [InstanceName]:
 #   Module: [ModuleName]
 #   Parameter1: Value
 #   Parameter2: Value

 # e.g.
Thrusters = '''
ThrusterFL:
     Name: FL
     Module: ThrusterOrder
     Address: 0x01
     Invert: true
ThrusterFR:
     Name: FR
     Module: ThrusterOrder
     Address: 0x02
     Invert: true
'''

import yaml
#d = None
#content = yaml.load(document)
#for data in content:
#    d = data
#    print(data)
    
content = yaml.load(open('config.yaml', 'r'))
print(content)

for nodeName in content:
    moduleName = content[nodeName]['Module']
    print(moduleName)

