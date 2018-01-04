import backend
import frontend
import notifier_plugin


def print_stuff(stuff):
    print(stuff)
    return f"I got {stuff}".encode()

plugin_manager = frontend.PluginManager()
# plugin_manager.register_plugin("printer", ["notification"],[print_stuff])
plugin_manager.register_plugin("Linux notifications", ["notification"], [notifier_plugin.create_notification])
server = backend.SSLServer(plugin_manager.handle_message)
