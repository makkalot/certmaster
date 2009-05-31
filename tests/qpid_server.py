from certmaster.connection.qpid.server import QpidRpcCertMaster
from certmaster.certmaster import CertMaster
from certmaster.connection.common import choose_current_server


SERVER_QUEUE = "localhost"

CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"
class SomeCustomCertmaster(CertMaster):
    def __init__(self, conf_file=CERTMASTER_CONFIG,connection_handler=None):
        super(SomeCustomCertmaster,self).__init__(conf_file,connection_handler)
        
        #some custom loading here
        self.handlers['echo_me']=self.echo_me

    def echo_me(self,some_stuff):
        return some_stuff


if __name__ == "__main__":
    print "Starting the qpid server"
    conn=choose_current_server(force_connection=QpidRpcCertMaster,cm_instance=SomeCustomCertmaster(),server_queue=SERVER_QUEUE)
    conn.start_serving()

