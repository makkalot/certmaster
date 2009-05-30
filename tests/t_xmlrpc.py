from certmaster.connection.xmlrpc.connection import XmlRpcConnection
from certmaster.connection.qpid.server import QpidRpcCertMaster
from certmaster.certmaster import CertMaster
from certmaster.connection.common import choose_current_connection

DEFAULT_TEST_PORT = 55555
DEFAULT_TEST_ADRR = "localhost"

SERVER_QUEUE = DEFAULT_TEST_ADRR

CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"
class SomeCustomCertmaster(CertMaster):
    def __init__(self, conf_file=CERTMASTER_CONFIG,connection_handler=None):
        super(SomeCustomCertmaster,self).__init__(conf_file,connection_handler)
        
        #some custom loading here
        self.handlers['echo_me']=self.echo_me

    def echo_me(self,some_stuff):
        return some_stuff


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "xmlrpc":
        print "Starting the xmlrpc server"
        conn=choose_current_connection(force_connection=XmlRpcConnection,cm_instance=SomeCustomCertmaster(),port=DEFAULT_TEST_PORT,listen_addr=DEFAULT_TEST_ADRR)
        conn.start_serving()
    elif sys.argv[1]=="qpid":
        print "Starting the qpid server"
        conn=choose_current_connection(force_connection=QpidRpcCertMaster,cm_instance=SomeCustomCertmaster(),server_queue=SERVER_QUEUE)
        conn.start_serving()
    else:
        print "No option like that exists"
        



