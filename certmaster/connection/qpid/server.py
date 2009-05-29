from connection import BaseQpidCertmasterServer


class EchoBigServer(BaseQpidCertmasterServer):

    def handle_custom_result(self,content):
        return str(content).upper()

class RpcServer(BaseQpidCertmasterServer):
    """
    That one will get some objects that contains callables
    or dictionary that contain callables
    """
    def __init__(self,*args,**kwargs):
        super(RpcServer,self).__init__(*args,**kwargs)
        
        if kwargs.has_key('callable_obj'):
            self.callables = kwargs['callable_obj']
        else:
            self.callables = None

        if kwargs.has_key('callable_dict'):
            self.callable_dict = kwargs['callable_dict']
        else:
            self.callable_dict = None


    def handle_custom_result(self,content):
        """
        The format of the content should be a dict
        with following inside it :
        {
            'callable_method':'method_name',
            'callable_module':'module_name'
            'args':[arg1,arg2,arg3]
        }
        """
        for callable in self.callables:
            print "Tha name of the callable is like ",callable.__class__.__name__.lower()
            if content['callable_module'] == callable.__class__.__name__.lower():
                if hasattr(callable,content['callable_method']):
                        return getattr(callable,content['callable_method'])(*content['args'])


        #we couldnt find the callable in the object stuff above
        #so should check the dictionary stuff that time
        for name,callable in self.callable_dict.iteritems():
            name = name.split(".")
            if name[0] == content['callable_module']:
                if name[1]==content['callable_method']:
                    return callable(*content['args'])


        return "Non existing error sorry , will return Exception in the future ... "
                    



class CallMe(object):
    
    def echo_int(self):
        return 100


def message(number):
    if number%2==0:
        return "Even Number"
    else:
        return "Odd Number"


class QpidRpcCertMaster(ConnectionInterface):
    pass



if __name__ == "__main__":
   rpc = RpcServer(callable_obj=[CallMe()],callable_dict={'system.message':message})
   rpc.serve()


