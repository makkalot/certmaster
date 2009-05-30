from certmaster.connection.common import choose_current_client
from certmaster.connection.xmlrpc.connection import XmlRpcClient
from certmaster.connection.qpid.client import QpidRpcClient

MASTER_URI = "http://localhost:55555"
def xml_rpc():
    s = choose_current_client(master_uri = MASTER_URI,force_connection=XmlRpcClient)
    # print "DEBUG: waiting for cert"
    for i in range(100):
        assert i == s.echo_me(i)
 
    for i in ["One","two","three"]:
        assert i == s.echo_me(i)

def test_qpid_rpc():
    s = choose_current_client(queue="localhost",force_connection=QpidRpcClient)
    # print "DEBUG: waiting for cert"
    for i in range(100):
        assert i == s.echo_me(i)
 
    for i in ["One","two","three"]:
        assert i == s.echo_me(i)

