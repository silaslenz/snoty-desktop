import logging
import backend
import frontend
import notifier_plugin

logging.basicConfig(level=logging.DEBUG)


def print_stuff(stuff):
    print(stuff)
    return f"I got {stuff}".encode()


# Register a plugin to manage incoming messages
plugin_manager = frontend.PluginManager()
# plugin_manager.register_plugin("printer", ["notification"],[print_stuff])  # Print notifications to console
plugin_manager.register_plugin("Linux notifications", ["notification"],
                               [notifier_plugin.create_notification])  # Show notifications as desktop notifications
server = backend.SSLServer(plugin_manager.handle_message)
