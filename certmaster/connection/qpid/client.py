from connection import BaseQpidClient
import utils

class QpidRpcClient(BaseQpidClient):
    """
    The qpid client that sends commands via broker to server
    """

    def __init__(self,*args,**kwargs):
        super(QpidRpcClient,self).__init__(*args,**kwargs)
        self.server_queue = kwargs.get('queue',None)
    
    def __getattr__(self,name):
        """
        Most of te time we will call stuff that is
        not there actually ..
        """
        return self.__CommandAutomagic(self,[name])
    

    
    class __CommandAutomagic(object):
        """
        This allows a client object to act as if it were one machine, when in
        reality it represents many.
        """

        def __init__(self, clientref, base):
            self.base = base
            self.clientref = clientref

        def __getattr__(self,name):
            base2 = self.base[:]
            base2.append(name)
            return __CommandAutomagic(self.clientref, base2)

        def __call__(self, *args):
            if not self.base:
                raise AttributeError("something wrong here")
            
            method = self.base[0]
            #send the actual data there
            return self.clientref.send_data(
                {
                    'module':None,
                    'method':method,
                    'args':args
                    },
                self.clientref.server_queue,
                return_result = True
                )

