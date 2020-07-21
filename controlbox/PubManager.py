import yaml
import ast
import re
import copy
import queue
import itertools
import time
from ModuleBase import Module
from pubsub import pub

#_____________________________________________
#HOW THIS WORKS
#Module send:
# if node is simply boolean
# then pub_to_manager(channel)
# Use pub_to_manager(channel, message = "") to send instruction to PubManager

#Module receive:
# Use pub.subscribe(self.listener, channel)
# def listener(self, arg):
#        self.var = arg


#TO DO

#Priority system:
#Node running
#If node with higher priority joins, suspend previous, run new, suspended previous value will be stored in last_inp
#Until timeout of new node or a node with higher priority appears

#If node with lower or equal priority joins, store there value as last_inp and continue current
#Until timeout of current and move on to highest priority among the low priority, using last_inp value

#Calculate timeout
#Refer to w_node
#Timeout nodes remove from current
#Add to will_remove
    #Main loop check inp_node
    #if inp_node priority higher, then switch inp_node to current and old node go to will_remove
    #lif inp_node priority lower or equal, then ignore and wait for timeout

'''
class Priority_Space():
    def __init__(self):
        self.__acc_time = 0
        self.__start_time = None
        self.__active = False

    @property
    def acc_time(self):
        return self.__acc_time

    @property
    def is_active(self):
        return self.__active

    def start_timer(self):
        if self.__start_time == None:
            self.__start_time = time.time()
            self.__active = True
        else:
            pass

    def accumulate_time(self):
        self.__acc_time = time.time()-self.__start_time

    def reset_acc_time(self):
        self.__acc_time = 0
        self.__start_time = None
        self.__active = False

    def times_up(self, node_timeout):
        if self.__acc_time>=node_timeout:
            return True
        return False

class W_Nodes():
    def __init__(self, name, priority, timeout, PrioritySpace):
        self.name = name
        self.priority = priority
        self.timeout = float(timeout)
        self.PrioritySpace = PrioritySpace
        self.__last_inp = None

    @property
    def last_inp(self):
        return self.__last_inp

    def handle_inp(self, inp):
        self.__last_inp = inp

    def check_time(self):
        return self.PrioritySpace.times_up(self.timeout)



class PriorityManager(Module):
    def __init__(self, w_nodes, priority_spaces):
        self.w_nodes = w_nodes    #{"Transect_Line": W_Node("Transect_Line", priority, timeout, PrioritySpace)}
        self.priority_spaces = priority_spaces
        self.current = []
        pub.subscribe(self.managerListener, 'PriorityManager')

    #receive node and it's respective value that is pubbed to other module
    def managerListener(self, nodename, nodevalue):
        self.w_nodes[nodename].handle_inp(nodevalue)

    def run(self):
        for priority_space in self.priority_spaces.values():
            priority_space.accumulate_time()
        for node in self.current:
            pass
            #Node timed out
            if self.w_nodes[node].check_time():
                #Check priority of each node in the priority space to determine which to be in current
                maximum = None
                for nodename, w_node_inst in self.w_nodes.items():
                    if w_node_inst.priority:
                        pass'''

#_____________________________________________

def pub_to_manager(channel, message = " "):
    #remove container character "[,],(,)"
    new_message = ""
    have_arg = False
    if type(message) == list or type(message)==tuple:
        new_message = " ,".join([str(item) for item in message if type(item)!=str])
        have_arg = True
    else:
        if type(message)!=str:
            new_message = str(message)
    #print(new_message)
    if have_arg:
        #pub.sendMessage('PubManager', instruction = f"%{channel}%[{message}]")
        pub.sendMessage("PubManager", instruction = "%"+channel+"%["+new_message+"]")
    else:
        #pub.sendMessage('PubManager', instruction = f"%{channel}%")
        pub.sendMessage("PubManager", instruction = "%"+channel+"%")

def sub_setting_var(text, setting_var):
    for i, j in setting_var.items():
        text = text.replace(i, j)
    return text

class PubManager(Module):
    def __init__(self, setting_file, show_default_plot = "False"):
        ###Setting Variables###
        self.setting_var = {"$HIGH$" : "1000",
                            "$MEDIUM$" : "100",
                            "$LOW$" : "10"}

        self.current = []
        self.will_remove = []
        self.f_node_remove = []
        self.previous_pub = {}
        self.nodes = []
        
        self.c_nodes = [] #cyclic
        self.r_nodes = [] #repeatable
        self.a_nodes = []
        self.f_nodes = [] #flicker
        self.edges = []
        #self.q = queue.Queue()
        pub.subscribe(self.managerListener, 'PubManager')

        #Read dict from yaml file
        content = yaml.load(open(setting_file, 'r'), Loader = yaml.FullLoader)
        for category, sub_category in content.items():
            if category=="Graph":
                for key, val in sub_category.items():
                    if key=="Nodes":
                        self.nodes = val#{key:(not value if type(value)==bool else value) for (key,value) in val.items()}
                        self.default_nodes = copy.deepcopy(val)
                        self.nodes_key = self.nodes.keys()

                        #Add $ALL$ as a setting variabale
                        self.setting_var["$ALL$"] = str(list(self.nodes_key))
                    
                    if key=="C_Nodes":
                        self.c_nodes = val
                    if key=="R_Nodes":
                        self.r_nodes = val
                    if key=="A_Nodes":
                        self.a_nodes = val
                    if key=="F_Nodes":
                        self.f_nodes = val
                    if key=="W_Nodes":
                        pass
                        '''
                        self.w_nodes = {}

                        self.priority_spaces = {priority_space_name:Priority_Space() for priority_space_name in val["Priority_Space"]}

                        w_entries = ast.literal_eval(sub_setting_var(str(val["Node_Entry"]), self.setting_var))
                        for entries in w_entries:
                            #Set last(priorityspace) value of list entries as the respective Priority_Space() class
                            entries[-1] = self.priority_spaces[entries[-1]]
                            #Key is nodename(first part of list), value is W_Node class(constructed with yaml and Priority_Space() class)
                            self.w_nodes[entries[0]]= W_Nodes(*entries)'''
                    if key== "Edges":
                        self.edges = []
                        for node1, node2 in val:
                            node1_list = []
                            node2_list = []
                            if bool(re.search(r'\$.*\$', node1)):
                                node1 = ast.literal_eval(sub_setting_var(node1, self.setting_var))
                            if type(node1)== list or type(node1) == tuple:
                                node1_list = node1
                            else:
                                node1_list.append(node1)
                                    
                            if bool(re.search(r'\$.*\$', node2)):
                                node2 = ast.literal_eval(sub_setting_var(node2, self.setting_var))
                            if type(node2)== list or type(node2) == tuple:
                                node2_list = node2
                            else:
                                node2_list.append(node2)
                            node_lists = [node1_list, node2_list]
                            for node_tuples in list(itertools.product(*node_lists)):
                                if len(node_tuples)>1:
                                    node_set = set(node_tuples)
                                    if len(node_set)>1:
                                        self.edges.append(node_set)
                        
                        #Set unconnected nodes for a_nodes
                        self.unconnected = {}
                        for a_node in self.a_nodes:
                            connected = {node for edge in self.edges for node in edge if a_node in edge}
                            self.unconnected[a_node] = [node for node in self.nodes if node not in connected]
        
        #Start a module to help to manage timeout of nodes
        #priority_manager = PriorityManager(copy.deepcopy(self.w_nodes), copy.deepcopy(self.priority_spaces))
        #priority_manager.start()

        #Pub default values
        for node in self.nodes_key:
            self.pub_to_node(node)

        #Set a_node default in current
        for node in self.a_nodes:
            self.current.append(node)


        #Show plot
        if show_default_plot == "True":
            import networkx as nx
            import matplotlib.pyplot as plt
            G=nx.Graph()
            edge_list = ([[list(l)[0]+'\n'+str(self.nodes[list(l)[0]]), list(l)[1]+'\n'+str(self.nodes[list(l)[1]])] for l in self.edges])
            G.add_edges_from([[list(l)[0]+'\n'+str(self.nodes[list(l)[0]]), list(l)[1]+'\n'+str(self.nodes[list(l)[1]])] for l in self.edges])
            pos = nx.spring_layout(G)

            nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color = [[0, 1, 0] for node in G.nodes()], node_size = 500)
            nx.draw_networkx_labels(G, pos)
            nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color= [0.498, 0, 1], arrows=False)

            plt.show()


    def managerListener(self, instruction):
        #self.q.put(instruction)
        self.current = list(set(self.current))
        inp = sub_setting_var(instruction, self.setting_var)
        will_pub = [] ###########################################
        self.will_remove = self.will_remove + self.f_node_remove
        self.f_node_remove = []
        inp_node= re.findall(r'\%([^]]*)\%', inp)[0]
        arg = re.findall(r'\[.*\]', inp)
        #Place node in will_remove if it is a f_node
        if inp_node in self.f_nodes:
            self.f_node_remove.append(inp_node)

        if len(arg)!=0: #There is a '[...]'
            if type(self.nodes[inp_node]) != bool and inp_node not in self.c_nodes:
                self.nodes[inp_node] = ast.literal_eval(arg[0])
            elif len(arg)==1 and (arg[0] == "[True]" or arg[0] == "[False]"):
                self.nodes[inp_node] = eval(arg[0][1:-1])
            elif inp_node in self.c_nodes:
                self.nodes[inp_node] = [self.nodes[inp_node][0],self.nodes[inp_node][0].index(arg[0][1:-1])]
            else:
                raise TypeError("Arguments supplied to a boolean node")
        else:
            val = self.nodes[inp_node]
            #invert bool if inp is boolean
            if type(val)==bool:
                self.nodes[inp_node] = not val
            #Increase the pointer index
            elif inp_node in self.c_nodes:
                val[1]= (val[1]+1)%len(val[0])
            else:
                raise TypeError("No arguments supplied for a non-boolean node")

        #Update previous_pub if nodevalue is new
        #if inp_node in self.previous_pub.keys() and self.nodes[inp_node]!=self.previous_pub[inp_node]:
        #    del self.previous_pub[inp_node]
        #    if inp_node in self.will_remove:
        #        self.will_remove.remove(inp_node)

        #Place node in will_remove if nodevalue is repeated
        if inp_node in self.previous_pub.keys() and self.nodes[inp_node]==self.previous_pub[inp_node]:
            self.will_remove.append(inp_node)

        #Place node in will_remove if node is in a deactivated state
        if inp_node not in (self.a_nodes+self.r_nodes):
            if self.nodes[inp_node] == self.default_nodes[inp_node]:
                self.will_remove.append(inp_node)

        if inp_node not in self.will_remove:
            if inp_node not in self.current:
                self.current.append(inp_node)
            for i in range(len(self.current)):
                #Prevent checking with itself
                if inp_node==self.current[i]:
                    continue
                #No need to remove a_nodes
                if self.current[i] in self.a_nodes:
                    continue
                #Remove disconnected nodes if inp_code is at a activated stated
                if self.nodes[inp_node]!=self.default_nodes[inp_node]:
                    if {inp_node, self.current[i]} not in self.edges:
                        self.will_remove.append(self.current[i])
        
        #print("activate_controller: ", self.nodes["activate_controller"])
        #print("activate_transectline:", self.nodes["activate_transectline"])
        #print("current: ", self.current)
        #print("will_remove:", self.will_remove)

        #Add a_node back in if no unconnected is present in current
        for node in self.a_nodes:
            for unconnected_node in self.unconnected[node]:
                #if a_nodes's unconnected node is a a_node itself
                if unconnected_node in self.a_nodes:
                    #if a_node's unconnected node is activated, deactivate a_node
                    if self.nodes[unconnected_node] == self.default_nodes[unconnected_node]:
                        self.nodes[node] = not copy.deepcopy(self.default_nodes)[node]
                        break
                    else:
                        self.nodes[node] = copy.deepcopy(self.default_nodes)[node]

                else:
                    #if a_node's unconnected node is activated, deactivate a_node
                    if self.nodes[unconnected_node] != self.default_nodes[unconnected_node]:
                        self.nodes[node] = not copy.deepcopy(self.default_nodes)[node]
                        break
                    else:
                        self.nodes[node] = copy.deepcopy(self.default_nodes)[node]
        

        #Remove and set nodes to default value, clear from previous_pub  
        for item in self.will_remove:
            self.nodes[item] = copy.deepcopy(self.default_nodes)[item]
            if item in self.previous_pub.keys():
                self.previous_pub.pop(item)
            
        
        
        
        #pub nodevalue to real node module
        for node in self.current:
            #Store pub value to previous_pub except for r_node and a_node
            if inp_node not in (self.r_nodes+self.a_nodes):
                self.previous_pub[inp_node] = copy.deepcopy(self.nodes)[inp_node]
            will_pub.append(node)
            #self.pub_to_node_and_manager(node)

        #Clear nodes from current
        for item in self.will_remove:
            if item in self.current:
                self.current.remove(item)

        #Clear will_remove
        self.will_remove = []
        
        
        for node in will_pub:
            self.pub_to_node(node)


    def showListener(self, message):
        self.show = message

    def c_node_value(self, c_node):
        return self.nodes[c_node][0][self.nodes[c_node][1]]

    def pub_to_node(self, node):
        if node in self.c_nodes:
            value = self.c_node_value(node)
        else:
            value = self.nodes[node]
        pub.sendMessage(node, message = value)

    def run(self):
        pass
