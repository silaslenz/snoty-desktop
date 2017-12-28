import backend
import frontend


def print_stuff(stuff):
    print(stuff)
    return f"I got {stuff}".encode()

plugin_manager = frontend.PluginManager()
plugin_manager.register_plugin("printer", ["notification"],[print_stuff])
server = backend.SSLServer(plugin_manager.handle_message)
