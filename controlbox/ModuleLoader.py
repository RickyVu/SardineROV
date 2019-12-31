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

    def loadfrom(file, module, name, frequency):
        exec("from " + str(file) + " import " + str(module))
        exec(str(name) + " = " + str(module) + "()")
        exec(str(name) + ".start(" + str(frequency) + ")")

    def load_byName(Names, YAML_File):
        for i in range(len(Names)):
            Names[i] = Names[i].lower()
            
        try:
            content = yaml.load(open(str(YAML_File), 'r'))
            for nodeName in content:
                args = ''
                if nodeName.lower() in Names:
                    moduleName = content[nodeName]
                    for key in moduleName:
                        value = moduleName[key]

                        #Required
                        if key == 'file':
                            file = value
                        elif key == 'varclass':
                            varclass = value
                        elif key == 'frequency':
                            frequency = value
                        #Exceptions
                        elif key == 'gui':
                            pass
                        #Arguments
                        else:
                            args = args + f"{key}='{value}',"

                    #Complete argument
                    try:
                        if args[-1] == ',':
                            args = args[:-1]
                    except IndexError:
                        pass

                    #Execute one node
                    exec(f"from {file} import {varclass}") 
                    exec(f"{nodeName} = {varclass}({args})")
                    print(f"{nodeName} successfully loaded")
                    exec(f"{nodeName}.start({frequency})")

        except FileNotFoundError:
            print('File not found')

    def load_all(YAML_File):
        try:
            content = yaml.load(open(str(YAML_File), 'r'))
            frequency = 1
            for nodeName in content:
                args = ''
                moduleName = content[nodeName]
                for key in moduleName:
                    value = moduleName[key]

                    #Required
                    if key == 'file':
                        file = value
                    elif key == 'varclass':
                        varclass = value
                    elif key == 'frequency':
                        frequency = value
                    #Exceptions
                    elif key == 'gui':
                        pass
                    #Arguments
                    else:
                        args = args + f"{key}='{value}',"

                #Complete argument
                try:
                    if args[-1] == ',':
                        args = args[:-1]
                except IndexError:
                    pass

                #Execute one node
                exec(f"from {file} import {varclass}") 
                exec(f"{nodeName} = {varclass}({args})")
                print(f"{nodeName} successfully loaded")
                exec(f"{nodeName}.start({frequency})")

        except FileNotFoundError:
            print('File not found')

    def load_gui(YAML_file, screen_width, screen_height):
        import pygame
        from GUI_Widget import ThrusterWidget
        class_name_list = []
        gui_loop = False
        try:
            content = yaml.load(open(str(YAML_file), 'r'))
            for nodeName in content:
                gui = False
                class_name = str(nodeName)+'_Widget'
                moduleName = content[nodeName]
                for key in moduleName:
                    value = moduleName[key]
                    if key == 'varclass':
                        varclass = str(value)
                    if key == 'gui':
                        if value == True:
                            gui = True
                            gui_loop = True
                if gui == True:
                    exec(f"{class_name} = {varclass}Widget(15, '{nodeName}')")
                    class_name_list = class_name_list + [str(nodeName)+'_Widget']
                    print(f"{class_name} successfully loaded")
            if gui_loop== True:
                pygame.init()
                screen = pygame.display.set_mode((screen_width, screen_height))
                while True:
                    screen.fill((0, 0, 0))
                    x = 0
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    for class_name in class_name_list:
                        exec(f"{class_name}.update(screen, ({x}, 0))")
                        x = x+80
                    pygame.display.flip()

            
        except FileNotFoundError:
            print('File not found')



