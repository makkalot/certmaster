from certmaster.connection.common import choose_current_client
from certmaster.connection.qpid.client import QpidRpcClient
#to run these tests here you should start your test qpid server which is in qpid_server.py
def test_qpid_rpc():
    s = choose_current_client(queue="localhost",force_connection=QpidRpcClient)
    # print "DEBUG: waiting for cert"
    for i in range(100):
        assert i == s.echo_me(i)
 
    for i in ["One","two","three"]:
        assert i == s.echo_me(i)

