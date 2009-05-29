import certmaster.codes as codes
import certmaster.logger as logger
from certmaster.config import read_config
from certmaster.commonconfig import CMConfig
from certmaster.commonconfig import CMConfig

from certmaster.certmaster import CertMaster
from certmaster.connection.common  import ConnectionInterface

CERTMASTER_LISTEN_PORT = 51235
CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"

import SimpleXMLRPCServer
class CertmasterXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):
    def __init__(self, addr):
        self.allow_reuse_address = True
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self, addr)


class XmlRpcConnection(ConnectionInterface):
    
    def __init__(self,*args,**kwargs):
        """
        The init stuff comes here
        """
        #the server instance will be the one that will 
        #do the general stuff
        self.certmaster=kwargs.get('certmaster',None)
        self.__port=kwargs.get('port',None)
        self.__listen_addr=kwargs.get('listen_addr',None)
        
        #will be set later
        self.__server_instance = None
    
    def set_server(self,*args,**kwargs):
        """
        Set the server instance here
        """

        config = read_config(CERTMASTER_CONFIG, CMConfig)
        listen_addr = self.__listen_addr or config.listen_addr
        listen_port = self.__port or config.listen_port
        if listen_port == '':
            listen_port = CERTMASTER_LISTEN_PORT 
 
        self.__server_instance = CertmasterXMLRPCServer((listen_addr,listen_port))
        self.__server_instance.logRequests = 0 # don't print stuff to console
        self.__server_instance.register_instance(self.certmaster)
        self.certmaster.logger.info("certmaster started on %s:%s"%(listen_addr,str(listen_port)))
        self.certmaster.audit_logger.logger.info("certmaster started on %s:%s"%(listen_addr,str(listen_port)))


    def set_callables(self,*args,**kwargs):
        """
        Set here callables ...
        """

        if not self.certmaster:
            self.certmaster = CertMaster(CERTMASTER_CONFIG,self)
        else:
            self.__set_connection_handler()

    def __set_connection_handler(self):
        """
        A private method for passing the conatiner reference to contaniee 
        """
        self.certmaster.set_chandler(self)

    def load_server_modules(self):
        """
        In that module you will be loading the modules
        that will be executed during remote calls
        """
        pass
    
    def pre_handle_method_call(self,method,params):
        """
        When you want to customize the behaviour of method 
        call that is the the place you should touch ...
        """
        pass 
    
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
        self.certmaster.logger.info("certmaster xmlrpc server serving")
        self.__server_instance.serve_forever()
