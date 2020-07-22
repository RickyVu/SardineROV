import logging
import csv
import time
from ModuleBase import Module
from pubsub import pub
import os
import sys
from itertools import islice

'''
class CsvFormatter(logging.Formatter):
    def __init__(self, log_file = None):
        super().__init__()
        self.output = log_file
        self.writer = csv.writer(open(self.output, "w"), quoting=csv.QUOTE_ALL)
        print("init formatter")

    def format(self, record):
        print(record)
        print("args", record.args)
        #print(record.levelname, record.msg)
        self.writer.writerow([record.levelname, record.msg])
        return record.msg
'''


class Logger(Module):
    def __init__(self, name = "Thruster_Output", log_file = None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        #self.logger.setLevel(getattr(logging, level.upper()))
        self.needs_header = True
        '''
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG) # log all escalated at and above DEBUG
        if log_file!= None:
            #logging.basicConfig(filename = log_file, level = logging.DEBUG)
            # add a file handler
            filehandler = logging.FileHandler(log_file)
            filehandler.setLevel(logging.DEBUG) # ensure all messages are logged to file

            # create a formatter and set the formatter for the handler.
            formatter = logging.Formatter('%(asctime)s,%(message)s')#datefmt='%m/%d/%Y %I:%M:%S')
            filehandler.setFormatter(formatter)

            # add the Handler to the logger
            self.logger.addHandler(filehandler)
        else:
            logging.basicConfig(format = '%(asctime)s,%(message)s', datefmt='%m/%d/%Y %I:%M:%S')
        '''
        pub.subscribe(self.MessageListener, 'Thruster Power Output')

        self.formatter = logging.Formatter(
            (
                '%(levelname)s,%(time)s,"%(address)s","%(value)s"'
            )
        )


        self.log_file = log_file
        if self.log_file:
            # create a channel for handling the logger (stderr) and set its format
            ch = logging.FileHandler(log_file)
        else:
            # create a channel for handling the logger (stderr) and set its format
            ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)

        # connect the logger to the channel
        self.logger.addHandler(ch)

        self.init_time = time.time()


    def log(self, msg, level='debug'):
        if self.needs_header:
            HEADER = 'levelname,time,address,value\n'
            if self.log_file and os.path.isfile(self.log_file):
                with open(self.log_file) as file_obj:
                    if len(list(islice(file_obj, 2))) > 0:
                        self.needs_header = False
                if self.needs_header:
                    with open(self.log_file, 'a') as file_obj:
                        file_obj.write(HEADER)
            else:
                if self.needs_header:
                    sys.stderr.write(HEADER)
            self.needs_header = False

        extra = {
            'time': str(time.time()-self.init_time),
            'address': str(msg[0]),
            'value': str(msg[1])
        }
        func = getattr(self.logger, level)
        func(msg, extra=extra)


    def MessageListener(self, pub): #pub[0] CAN address, pub[1] thruster power -32768 to 32767
        CAN_address = str(pub[0])
        power = str(pub[1])
        #log_data = f'{CAN_address},{power}'
        #logging.debug(" CAN address: {}      Power: {}".format(self.CAN_address, self.power))
        #self.logger.debug(msg = '%s,%s,%d',CAN_address, power, )
        self.log(pub, level='info')

    def run(self):
        pass

