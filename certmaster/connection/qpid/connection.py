import qpid
import sys
import os
from qpid.util import connect
from qpid.connection import Connection
from qpid.datatypes import Message, RangedSet, uuid4
from qpid.queue import Empty

#----- Initialization -----------------------------------
import utils as ut
import simplejson as json
import certmaster.logger as log
#  Set parameters for login

BROKER="127.0.0.1"
BROKER_PORT=5672
BROKER_USER="guest"
BROKER_PASS="guest"

CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"
class QpidConnection(object):
    """
    A simple Qpid connection
    """
    
    def __init__(self,conf_file = None,broker=None,broker_port=None,broker_user=None,broker_pass=None,*args,**kwargs):
        if not conf_file:
            self.config = read_config(CERTMASTER_CONFIG, CMConfig)
        else:
            self.config = read_config(conf_file, CMConfig)


        self.broker = broker or self.config.broker or BROKER
        self.broker_port = broker_port or self.config.broker_port or BROKER_PORT
        self.broker_user = broker_user or self.config.broker_user or BROKER_USER
        self.broker_pass = broker_pass or self.config.broker_pass BROKER_PASS
       
        #set Up a logger
        self.logger = log.Logger().logger
        #the conneciton status
        self.conenction_status = False
        self.__setup_connection()

    def __setup_connection(self):
        """
        Set up a connection
        """
        socket = connect(self.broker,self.broker_port)
        self.connection = Connection (sock=socket, username=self.broker_user, password=self.broker_pass)
        self.connection.start()
        self.session = self.connection.session(str(uuid4()))
        self.conenction_status = True
        self.logger.info("Client connected to broker %s:%s with username :%s"%(self.broker,self.broker_port,self.broker_user))

    def close_connection(self):
        """
        Closing the started connection
        """
        self.session.close(timeout=10)
        self.conenction_status = False
        self.logger.info("Client closing connection to broker %s:%s with username :%s"%(self.broker,self.broker_port,self.broker_user))


class BaseQpidCertmasterServer(QpidConnection):
    """
    The server side that waits on the Overlord part
    """

    QUEUE_NAME = "certmaster_%s"%ut.get_host()
    LOCAL_QUEUE = "certmaster_%s_local"%ut.get_host()
    BINDING_KEY = QUEUE_NAME


    def __init__(self,*args,**kwargs):
        super(BaseQpidCertmasterServer,self).__init__(*args,**kwargs)
        #you can set Up the queue dynamically
        self.server_queue = kwargs.get('server_queue',QUEUE_NAME)
        self.binding_key = self.server_queue


    def serve(self):
        self.session.queue_declare(queue=self.server_queue, exclusive=True)
        self.session.exchange_bind(exchange="amq.direct", queue=self.server_queue, binding_key=self.binding_key)

        local_queue_name = self.LOCAL_QUEUE
        self.session.message_subscribe(queue=self.server_queue, destination=local_queue_name)

        queue = self.session.incoming(local_queue_name)
        queue.start()
        #declare a method to handle the incoming output
        queue.listen(self.handle_result)
        
        self.logger.info("Certmaster starts serving on queue :%s "%(self.server_queue))
        import time
        while self.is_connection_open():
            #listen here for incoming messages
            time.sleep (1)

    
    def handle_result(self,message):
        """
        Handles the connection
        """
        content = json.loads(str(message.body))
        self.session.message_accept(RangedSet(message.id)) 

        message_properties = message.get("message_properties")
        reply_to = message_properties.reply_to
        if reply_to == None:
            raise Exception("This message is missing the 'reply_to' property, which is required")
        
        self.logger.info("Certmaster recieved request from %s with message %s"%(reply_to["routing_key"],content))
        #call the custom handle
        return_result = json.dumps(self.handle_custom_result(content))
        #transfer the stuff back to client
        props = self.session.delivery_properties(routing_key=reply_to["routing_key"]) 
        self.session.message_transfer(destination=reply_to["exchange"], message=Message(props,return_result))
        self.logger.info("Certmaster answered the  request from %s with message %s"%(reply_to["routing_key"],return_result))

    def handle_custom_result(self,content):
        """
        To be overriden by client applications
        """
        return content


    def is_connection_open(self):
        return self.conenction_status


class BaseQpidCertmasterClient(QpidConnection):
    """
    The client part which is on the minions
    """
    CLIENT_QUEUE = "certmaster_client_%s_%s"

    def __init__(self,*args,**kwargs):
        super(BaseQpidCertmasterClient,self).__init__(*args,**kwargs)
        self.reply_to = None

    def __start_connection(self):
        """
        You declare here the main stuff to conenct to the server
        """
        #here you declare a queue to wait for server result
        self.reply_to = self.CLIENT_QUEUE%(ut.get_host(),self.session.name)
        self.session.queue_declare(queue=self.reply_to, exclusive=True)
        self.session.exchange_bind(exchange="amq.direct", queue=self.reply_to, binding_key=self.reply_to)
        local_queue_name = "local_queue"
        self.local_queue = self.session.incoming(local_queue_name)

        #start your queue there
        self.session.message_subscribe(queue=self.reply_to, destination=local_queue_name)
        self.local_queue.start()
        
        self.logger.info("Certmaster client subscribed to queue %s "%(self.reply_to))
        

    def __send_request(self,data,queue_name):
        """
        Sending the request
        """
        #set the delivery options
        message_properties = self.session.message_properties()
        message_properties.reply_to = self.session.reply_to("amq.direct", self.reply_to)
        delivery_properties = self.session.delivery_properties(routing_key=queue_name)
        
        #sometimes we dont want to call the custom method just want to pass the stuff
        to_send = json.dumps(self.send_custom_request(data))

        #sending message
        self.session.message_transfer(destination="amq.direct", message=Message(message_properties, delivery_properties,to_send))
        self.logger.info("Certmaster client sent message: %s to: %s"%(to_send,queue_name))
        
        #recieving data from server
        return self.__process_result()

    def send_custom_request(self,data,*args,**kwargs):
        """
        Tobe overriden,prepare here your data that want to send 
        and return it back after that ...
        """
        return data

    def __process_result(self):
        """
        Processes the result here
        """
        #get the message
        message = self.local_queue.get(timeout=1000)
        content = json.loads(message.body)
        self.session.message_accept(RangedSet(message.id))
        processed = self.process_custom_result(content)
        self.logger.info("Certmaster client recieved message from server %s"%(content))
       
        return processed

    def process_custom_result(self,result,*args,**kwargs):
        """
        Method should be overriden,here do the stuff you want
        to do with data that comes back from the server ...
        """
        return result

    def send_data(self,data,queue_name,return_result=False):
        """
        That is the method toy should call when using that class
        """
        #set up your own queue
        if not self.reply_to:
            self.__start_connection()
        if return_result:
            return self.__send_request(data,queue_name)
        else:
            self.__send_request(data)

