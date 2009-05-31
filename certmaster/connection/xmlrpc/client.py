import xmlrpclib
from certmaster.connection.common  import ClientInterface

class XmlRpcClient(ClientInterface):
    """
    Client XmlRpcSender
    """ 
    def __init__(self,*args,**kwargs):
        self.master_uri = kwargs.get('master_uri','localhost')
        self.client = xmlrpclib.ServerProxy(self.master_uri)

    def __getattr__(self,name):
        """
        Just a proxy method 
        """
        return getattr(self.client,name)


