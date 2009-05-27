from connection import BaseQpidCertmasterClient
import utils

class LineSender(BaseQpidCertmasterClient):

    def send_custom_request(self,data,*args,**kwargs):
        """
        Here will append a newline to every new one
        """
        return str(data)+" line "

    def process_custom_result(self,result,*args,**kwargs):
        """
        Here will add the stuff
        """
        return " processed ! "+str(result) 


class RpcSender(BaseQpidCertmasterClient):
    pass


if __name__ == "__main__":
    #l=LineSender()
    
    #for i in ["One","Two","Three","Four","Five"]:
    #    tmp_res = l.send_data(i,"certmaster_%s"%utils.get_host(),True)
    #    print "THE returning final result is like ",tmp_res
    r =RpcSender()
    tmp_dict = {
            
            'callable_method':'echo_int',
            'callable_module':'callme',
            'args':[]
            }

    print "The result from CallMe.echo_int is ",r.send_data(tmp_dict,"certmaster_%s"%utils.get_host(),True)
    
    tmp_dict = {
            
            'callable_method':'message',
            'callable_module':'system',
            'args':[100]
            }


    print "The result from CallMe.echo_int is ",r.send_data(tmp_dict,"certmaster_%s"%utils.get_host(),True)
