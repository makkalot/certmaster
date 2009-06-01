import certmaster.logger as logger
class ServerInterface(object):
    
    def __init__(self,*args,**kwargs):
        """
        The init stuff comes here
        """
        self.logger = logger.Logger().logger
        self.audit_logger = logger.AuditLogger()
    
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
        pass

class ClientInterface(object): 
    
    def __init__(self,*args,**kwargs):
        """
        The init stuff comes here
        """
        self.logger = logger.Logger().logger
        self.audit_logger = logger.AuditLogger()
    


CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"
from certmaster.commonconfig import CMConfig
from certmaster.config import read_config

def choose_current_server(conf_file=None,force_connection=None,cm_instance=None,port=None,listen_addr=None,server_queue=None):
    """
    Choses the right connection from conf file and starts
    it according to that stuff ....
    """
    from certmaster.connection.xmlrpc.server import XmlRpcCertMaster
    from certmaster.connection.qpid.server import QpidRpcCertMaster
    
    if not conf_file:
        config = read_config(CERTMASTER_CONFIG, CMConfig)
    else:
        config = read_config(conf_file, CMConfig)
    
    #sometimes you may need passing the connection yourself
    if force_connection:
        return force_connection(certmaster=cm_instance,port=port,listen_addr=listen_addr,server_queue=server_queue)

    connection = config.connection
    if not connection:
        connection = "xmlrpc"

    if connection == "xmlrpc":
        return XmlRpcCertMaster()
    elif connection == "qpid":
        return QpidRpcCertMaster()

    return None


def choose_current_client(conf_file=None,master_uri=None,force_connection=None,queue=None):
    """
    Same as above but for client
    """
    from certmaster.connection.xmlrpc.client import XmlRpcClient
    from certmaster.connection.qpid.client import QpidRpcClient

    if not conf_file:
        config = read_config(CERTMASTER_CONFIG, CMConfig)
    else:
        config = read_config(conf_file, CMConfig)
    
    #sometimes you may need passing the connection yourself
    if force_connection:
        return force_connection(master_uri=master_uri,queue=queue)

    connection = config.connection
    if not connection:
        connection = "xmlrpc"

    if connection == "xmlrpc":
        return XmlRpcClient(master_uri=master_uri)
    elif connection == "qpid":
        return QpidRpcClient(queue=queue)

    return None

MINION_CONF = '/etc/certmaster/minion.conf'
from certmaster.commonconfig import MinionConfig
def get_certmaster_adress():
    """
    An client util method
    """

    config = read_config(MINION_CONF, MinionConfig)
    if config.connection == "xmlrpc":
        return 'http://%s:%s/' % (config.certmaster, config.certmaster_port)
    elif config.connection == "qpid":
        return config.certmaster
    else:
        return None


