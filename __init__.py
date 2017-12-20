import backend


def print_stuff(stuff):
    print(stuff)
    return f"I got {stuff.decode('utf-8')}".encode()


server = backend.SSLServer(print_stuff)
