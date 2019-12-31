from pubsub import pub
import yaml
from ModuleBase import Module
from threading import Timer
#from Thruster_Message import Thruster

class Loader():  #  30,   FL, Thruster_Message, Thruster, 0x011, True
    def manual_load(name, file, varclass, args, frequency=1):
        exec('from '+file+' import '+varclass) 
        exec(name+'='+varclass+"('"+name+"',"+str(args)+')')
        exec(name+'.start('+str(frequency)+')')

    def load_all(YAML_file):
        try:
            content = yaml.load(open(str(YAML_file), 'r'))
            frequency = 1
            for nodeName in content:
                args = ''
                Counter = 1
                args = args + "name='" + str(nodeName)+"',"
                moduleName = content[nodeName]
                for key in moduleName:
                    value = moduleName[key]
                    Counter+=1
                    if key=='frequency':
                        frequency = int(value)
                    elif key=='file':
                        file = str(value)
                    elif key=='varclass':
                        varclass = str(value)
                        Counter-=1
                    elif key=='address' and Counter == len(content[nodeName]):
                        args = args + key+"="+hex((moduleName[key]))
                    elif key=='address':
                        args = args + key+"="+hex((moduleName[key]))+","
                    elif Counter == len(content[nodeName]):
                        args = args + key+"='"+str(value)+"'"
                    else:
                        args = args + key+"='"+str(value)+"',"
                exec('from '+file+' import '+varclass) 
                exec(nodeName+'='+varclass+"("+args+")")
                print(nodeName,'successfully loaded')
                exec(nodeName+'.start('+str(frequency)+')')
        except FileNotFoundError:
            print('File not found')

    def load_byName(Name, YAML_file, frequency):
        try:
            content = yaml.load(open(str(YAML_file), 'r'))
            args = ''
            Counter = 0
            for nodeName in content:
                if Name.lower() == nodeName.lower():
                    args = args + "name='" + str(nodeName)+"',"
                    moduleName = content[nodeName]
                    for key in moduleName:
                        Counter+=1
                        value = moduleName[key]
                        if key== 'frequency':
                            frequency = value
                        elif key=='file':
                            file = str(value)
                        elif key=='varclass':
                            varclass = str(value)
                            Counter-=1
                        elif key=='address' and Counter == len(content[nodeName]):
                            args = args + key+"="+hex((moduleName[key]))
                        elif key=='address':
                            args = args + key+"="+hex((moduleName[key]))+","


                        elif key=='gui':
                            pass

                            
                        elif Counter == len(content[nodeName]):
                            args = args + key+"='"+str(value)+"'"
                        else:
                            args = args + key+"='"+str(value)+"',"
                    exec('from '+file+' import '+varclass) 
                    exec(nodeName+'='+varclass+"("+args+")")
                    print(nodeName,'successfully loaded')
                    exec(nodeName+'.start('+str(frequency)+')')
                    break
                else:
                    print('Name not found')
        except FileNotFoundError:
            print('File not found')

    def loadfrom(file, module, name, frequency):
        exec("from " + str(file) + " import " + str(module))
        exec(str(name) + " = " + str(module) + "()")
        exec(str(name) + ".start(" + str(frequency) + ")")
    '''
    def load_gui(YAML_file, screen_width, screen_height):
        import pygame
        from GUI_Widget import ThrusterWidget
        class_name_list = []
        try:
            content = yaml.load(open(str(YAML_file), 'r'))
            for nodeName in content:
                gui = False
                class_name = str(nodeName)+'_Widget'
                class_name_list = class_name_list + [str(nodeName)+'_Widget']
                moduleName = content[nodeName]
                for key in moduleName:
                    value = moduleName[key]
                    if key == 'varclass':
                        varclass = str(value)
                    if key == 'gui' and value == 'True':
                        gui = True
                if gui == True:
                    exec(f"{class_name} = {varclass}Widget(15, {nodeName})")
                    print(f"{class_name} successfully loaded")

            pygame.init()
            screen = pygame.display.set_mode((screen_width, screen_height))
            while True:
                x = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                for class_name in class_name_list:
                    exec(f"{class_name}.update(screen, ({x}, 0))")
                    x = x+50
                pygame.display.flip()

            
        except FileNotFoundError:
            print('File not found')
    '''


#Loader.loadfrom("Gamepad_Normalize", "Gamepad", "gp", "10000")
#Loader.loadfrom("Thruster_Profile", "FormulaApply", "fa","100")
#Loader.manual_load('FL', 'Thruster_Message', 'Thruster', "0x011,True", 10)
#Loader.load_byName('ThrusterFR', 'config.yaml',10)
#Loader.load_all('config.yaml', 10)
#from Test import Thruster
#Loader.load_controls(10000, 10000)
#Loader.load_all('config_test.yaml', 10)
#Loader.load_byName('ThrusterFR', 'config_test.yaml',10)
