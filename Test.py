import yaml
from ModuleLoader import Loader
'''
B = 30
A = 0

if A >=0:
    print(1/B*(((B+1)**A)-1))
elif A<0:
    print(-1/B*(((B+1)**-A)-1)) 

import yaml
from YAML_Test import Thrusters

content = yaml.load(Thrusters)
print(content['ThrusterFL'])

def Add(X, Y, Z=0):
    return X+Y+Z

print(Add(10, 10))
'''
'''
try:
    content = yaml.load(open(str('config.yaml'), 'r'))
    Name = 'ThrUsterfL'
    List = []
    Counter = 1
    for nodeName in content:
        if Name.lower() == nodeName.lower():
            List = List + ["Name='" + str(nodeName)+"'"]
            moduleName = content[nodeName]
            for key in moduleName:
                Counter+=1
                value = moduleName[key]
                if key=='file' or key=='varclass':
                    exec(str(key)+"='"+str(value)+"'")
                elif key=='address':
                    List = List + [key+"='"+hex((moduleName[key]))+"'"]
                elif Counter == len(content[nodeName]):
                    List = List + [key+"='"+str(value)+"'"]
                else:
                    List = List + [key+"='"+str(value)+"'"]
            a = tuple(List)
            #print(*List)
            #exec('from '+file+' import '+varclass)
            #exec(nodeName+'='+varclass+','+str(a))

            break
        else:
            print('Name not found')
except FileNotFoundError:
    print('File not found')
Loader.loadAll('config.yaml')
'''
