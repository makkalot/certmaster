from certmaster.connection.xmlrpc.connection import XmlRpcConnection
from certmaster.certmaster import CertMaster
from certmaster.connection.common import choose_current_connection

DEFAULT_TEST_PORT = 55555
DEFAULT_TEST_ADRR = "localhost"

CERTMASTER_CONFIG = "/etc/certmaster/certmaster.conf"
class SomeCustomCertmaster(CertMaster):
    def __init__(self, conf_file=CERTMASTER_CONFIG,connection_handler=None):
        super(SomeCustomCertmaster,self).__init__(conf_file,connection_handler)
        
        #some custom loading here
        self.handlers['echo_me']=self.echo_me

    def echo_me(self,some_stuff):
        return some_stuff


if __name__ == "__main__":
    conn=choose_current_connection(force_connection=XmlRpcConnection,cm_instance=SomeCustomCertmaster(),port=DEFAULT_TEST_PORT,listen_addr=DEFAULT_TEST_ADRR)
    conn.start_serving()


