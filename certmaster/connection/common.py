class ConnectionInterface(object):
    
    def __init__(self,*args,**kwargs):
        """
        The init stuff comes here
        """

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



class QpidConnection(ConnectionInterface):
    pass


CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"
from config import read_config
def choose_current_connection(conf_file):
    """
    Choses the right connection from conf file and starts
    it according to that stuff ....
    """

    from certmaster.connection.xmlrpc.connection import XmlRpcConnection
    #from certmaster.connection.qpid.connection import XmlRpcConnection
    config = read_config(CERTMASTER_CONFIG, CMConfig)
    connection = config.connection
    if not connection:
        connection = "xmlrpc"

    if connection == "xmlrpc":
        return XmlRpcConnection()
    elif connection == "qpid":
        return XmlRpcConnection()

    return None


