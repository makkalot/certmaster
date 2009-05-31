from connection import BaseQpidServer
from certmaster.connection.common  import ServerInterface


CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"
class QpidRpcCertMaster(ServerInterface,BaseQpidServer):
    """
    That one will get some objects that contains callables
    or dictionary that contain callables
    """
    def __init__(self,*args,**kwargs):
        """
        A place to insert some initialization
        """
        
        BaseQpidCertmasterServer.__init__(self,*args,**kwargs)
        ConnectionInterface.__init__(self,*args,**kwargs)

        #the certmaster here
        self.certmaster=kwargs.get('certmaster',None)
        
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


    def handle_custom_result(self,content):
        """
        The format of the content should be a dict
        with following inside it :
        {
            'method':'method_name',
            'module':'module_name'
            'args':[arg1,arg2,arg3]
        }
        """
        return self.certmaster.handle_method_call(
                content['method'],
                content['args'],
                )

    def start_serving(self):
        """
        Start the serving here
        """
        #set the certmaster
        self.__set_callables()
        self.certmaster.logger.info("certmaster QPID server serving")
        self.serve()



if __name__ == "__main__":
    pass

