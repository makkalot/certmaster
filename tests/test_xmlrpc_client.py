import xmlrpclib

MASTER_URI = "http://localhost:55555"
def test_xml_rpc():
    s = xmlrpclib.ServerProxy(MASTER_URI)
    # print "DEBUG: waiting for cert"
    for i in range(100):
        print i
        assert i == s.echo_me(i)
