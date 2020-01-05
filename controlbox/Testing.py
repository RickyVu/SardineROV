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
def Add(X, Y= 30):
    return X+Y

print(Add(10))
'''
while True:
    from inputs import get_gamepad
    events= get_gamepad()
    for event in events:
        analogcode = event.code[0:6]
        #print(event.code)
        if analogcode == 'BTN_TL':
            print(event.state)
