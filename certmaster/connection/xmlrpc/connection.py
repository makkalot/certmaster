import codes
import logger
from config import read_config
from commonconfig import CMConfig

from certmaster.connection.common import ConnectionInterface

CERTMASTER_LISTEN_PORT = 51235
CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"


class XmlRpcConnection(ConnectionInterface):
    
    def __init__(self,*args,**kwargs):
        """
        The init stuff comes here
        """
        #the server instance will be the one that will 
        #do the general stuff
        self.__server_instance = None
        self.__certmaster = None 
    
    def set_server(self,*args,**kwargs):
        config = read_config(CERTMASTER_CONFIG, CMConfig)
        listen_addr = config.listen_addr
        listen_port = config.listen_port
        if listen_port == '':
            listen_port = CERTMASTER_LISTEN_PORT 
 

        self.__server_instance = CertmasterXMLRPCServer((listen_addr,listen_port))
        self.__server_instance.logRequests = 0 # don't print stuff to console
        self.__server_instance.register_instance(self.__certmaster)
        self.__certmaster.logger.info("certmaster started")
        self.__certmaster.audit_logger.logger.info("certmaster started")


    
    def set_callables(self,*args,**kwargs):
        pass
        self.__certmaster = CertMaster(CERTMASTER_CONFIG)

    def load_server_modules(self):
        """
        In that module you will be loading the modules
        that will be executed during remote calls
        """
        
        #we get the certmaster object and set its handlers
        self.__certmaster.handlers={
                 'wait_for_cert': self.certmaster.wait_for_cert,
                 }
    
    def handle_method_call(self,method,params):
        """
        When you want to customize the behaviour of method 
        call that is the the place you should touch ...
        """
        if method == 'trait_names' or method == '_getAttributeNames':
            return self.__certmaster.handlers.keys()


        if method in self.__certmaster.handlers.keys():
            return self.__certmaster.handlers[method](*params)
        else:
            self.logger.info("Unhandled method call for method: %s " % method)
            raise codes.InvalidMethodException
    
    def start_serving(self):
        """
        Start the serving here
        """
        #set the certmaster
        self.set_callables()
        #load the modules
        self.load_server_modules()
        #set the server stuff
        self.set_server()
        #start serving 
        self.__server_instance.serve_forever()
       

     
import SimpleXMLRPCServer
class CertmasterXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):
    def __init__(self, addr):
        self.allow_reuse_address = True
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self, addr)


