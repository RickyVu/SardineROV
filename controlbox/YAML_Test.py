import yaml

    
content = yaml.load(open('config.yaml', 'r'))
print(content)

for nodeName in content:
    moduleName = content[nodeName]#['Invert']
    #print(len(content[nodeName])) #4
    #print('\n', list(content[nodeName].keys())[0]) #File
    #print(nodeName)  ThrusterFL
    print(type(moduleName))
        

