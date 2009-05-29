class ConnectionInterface(object):
    
    def __init__(self,*args,**kwargs):
        """
        The init stuff comes here
        """
        self.logger = logger.Logger().logger
        self.audit_logger = logger.AuditLogger()
    
    def load_server_modules(self):
        """
        In that module you will be loading the modules
        that will be executed during remote calls
        """
        pass


    def start_serving(self):
        """
        Start the serving here
        """
        pass

    
    def stop_server(self):
        """
        Stop the serving here
        """
        pass

class ClientInterface(object): 
    
    def __init__(self,*args,**kwargs):
        """
        The init stuff comes here
        """
        self.logger = logger.Logger().logger
        self.audit_logger = logger.AuditLogger()
    

class QpidConnection(ConnectionInterface):
    pass


CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"
from certmaster.commonconfig import CMConfig
from certmaster.config import read_config

def choose_current_connection(conf_file=None,force_connection=None,cm_instance=None,port=None,listen_addr=None):
    """
    Choses the right connection from conf file and starts
    it according to that stuff ....
    """
    from certmaster.connection.xmlrpc.connection import XmlRpcConnection
    #from certmaster.connection.qpid.connection import XmlRpcConnection
    if not conf_file:
        config = read_config(CERTMASTER_CONFIG, CMConfig)
    else:
        config = read_config(conf_file, CMConfig)
    
    #sometimes you may need passing the connection yourself
    if force_connection:
        print "Forcing the connection "
        return force_connection(certmaster=cm_instance,port=port,listen_addr=listen_addr)

    connection = config.connection
    if not connection:
        connection = "xmlrpc"

    if connection == "xmlrpc":
        return XmlRpcConnection()
    elif connection == "qpid":
        return XmlRpcConnection()

    return None


def choose_current_client(conf_file=None,master_uri=None,force_connection=None):
    """
    Same as above but for client
    """
    from certmaster.connection.xmlrpc.connection import XmlRpcClient

    if not conf_file:
        config = read_config(CERTMASTER_CONFIG, CMConfig)
    else:
        config = read_config(conf_file, CMConfig)
    
    #sometimes you may need passing the connection yourself
    if force_connection:
        return force_connection(master_uri=master_uri)

    connection = config.connection
    if not connection:
        connection = "xmlrpc"

    if connection == "xmlrpc":
        return XmlRpcClient(master_uri=master_uri)
    elif connection == "qpid":
        return XmlRpcClient(master_uri=master_uri)

    return None


