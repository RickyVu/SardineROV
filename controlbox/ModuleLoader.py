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
            content = yaml.load(open(str(YAML_File), 'r'), Loader = yaml.FullLoader)
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
                    try:
                        exec(f"from {file} import {varclass}") 
                        exec(f"{nodeName} = {varclass}({args})")
                        exec(f"{nodeName}.start({frequency})")
                        print(f"{nodeName} successfully loaded")
                    except:
                        print(f"{nodeName} failed to load")

        except FileNotFoundError:
            print('File not found')

    def load_all(YAML_File):
        nodes = []
        try:
            content = yaml.load(open(str(YAML_File), 'r'), Loader = yaml.FullLoader)
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
                _node = eval(varclass +"(" + args +")")
                nodes.append( { "node": _node, "clazz": varclass, "frequency": frequency, "args": args} )
                print(f"{nodeName} successfully loaded")
                # exec(f"{nodeName}.start({frequency})")
        except FileNotFoundError:
            print('File not found')
        return nodes

    def load_gui(YAML_file, screen_width, screen_height):
        import pygame
        from GUI_Widget import ThrusterWidget
        object_list = []
        gui_loop = False
        try:
            content = yaml.load(open(str(YAML_file), 'r'), Loader = yaml.FullLoader)
            for nodeName in content:
                gui = False
                instance_name = str(nodeName)+'_Widget'
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
                    exec(f"{instance_name} = {varclass}Widget('{nodeName}')")
                    object_list.append(eval(instance_name))
                    print(f"{instance_name} successfully loaded")
                    
            if gui_loop== True:
                pygame.init()
                screen = pygame.display.set_mode((screen_width, screen_height))
                while True:
                    screen.fill((0, 0, 0))
                    x = 0
                    y = 0
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    for objects in object_list:
                        screen.blit(objects.update(), (x,y))
                        x = x+ objects.getDimension()[0]
                    pygame.display.flip()

            
        except FileNotFoundError:
            print('File not found')



