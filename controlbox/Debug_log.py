import logging
import csv
import time
from ModuleBase import Module
from pubsub import pub


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



class Logger(Module):
    def __init__(self, log_file = None):
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

        
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        filehandler = logging.FileHandler(log_file)
        filehandler.setFormatter(CsvFormatter(log_file))
        self.logger.addHandler(filehandler)
        self.init_time = time.time()
        #logging.root.handlers[0].setFormatter(CsvFormatter(log_file))
        #self.logger.debug("srgdthy")



    def MessageListener(self, pub): #pub[0] CAN address, pub[1] thruster power -32768 to 32767
        CAN_address = str(pub[0])
        power = str(pub[1])
        #log_data = f'{CAN_address},{power}'
        #logging.debug(" CAN address: {}      Power: {}".format(self.CAN_address, self.power))
        #self.logger.debug(msg = '%s,%s,%d',CAN_address, power, )

    def run(self):
        pass

