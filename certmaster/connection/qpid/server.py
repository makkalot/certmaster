from connection import BaseQpidCertmasterServer


class EchoBigServer(BaseQpidCertmasterServer):

    def handle_custom_result(self,content):
        return str(content).upper()

if __name__ == "__main__":
    e = EchoBigServer()
    e.serve()

