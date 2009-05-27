import certmaster.utils

def get_host():
    """
    Simple util here
    """

    name = certmaster.utils.get_hostname(talk_to_certmaster=False)

    if name == "127.0.0.1":
        return "localhost"
    return name

