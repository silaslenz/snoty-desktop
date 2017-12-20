import backend


def print_stuff(stuff):
    print(stuff)


server = backend.SSLServer(print_stuff)

