from ModuleLoader import Loader
import Gamepad_ThrusterOrder as ThrusterOrder
import yaml
content = yaml.load(open('config.yaml', 'r'))
def KeyName(Dict, Iter):
    Count = 0
    for x in Dict:
        Count = Count +1
        if Count == Iter:
            return x
print(len(content)) #return 2
print(content)
print(KeyName(content, 2)) #return ThrusterFR
print(content[KeyName(content, 1)]['Module'])

for i in range(len(content)):
    Loader.load(str(content[KeyName(content, i+1)]['Module']), KeyName(content, i+1), 0, 'Thruster',content[KeyName(content, i+1)]['Address'], content[KeyName(content, i+1)]['Invert'])

