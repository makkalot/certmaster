import certmaster.codes as codes
import certmaster.logger as logger
from certmaster.config import read_config
from certmaster.commonconfig import CMConfig

from certmaster.certmaster import CertMaster
from certmaster.connection.common  import ServerInterface,ClientInterface

CERTMASTER_LISTEN_PORT = 51235
CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"

import SimpleXMLRPCServer
class CertmasterXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):
    def __init__(self, addr):
        self.allow_reuse_address = True
        SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self, addr)


class XmlRpcCertMaster(ServerInterface):
    
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
    
    def __set_server(self,*args,**kwargs):
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


    def __set_callables(self,*args,**kwargs):
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
    
    def start_serving(self):
        """
        Start the serving here
        """
        #set the certmaster
        self.__set_callables()
        #set the server stuff
        self.__set_server()
        #start serving 
        self.certmaster.logger.info("certmaster xmlrpc server serving")
        self.__server_instance.serve_forever()

