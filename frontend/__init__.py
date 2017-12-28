import json

class PluginManager:
    def __init__(self):
        self.plugins = {}

    def register_plugin(self, name, types, functions):
        self.plugins[name] = {}
        self.plugins[name]["types"] = types
        self.plugins[name]["functions"] = functions

    def deregister_plugin(self, name):
        self.plugins.remove(name)

    def find_plugin_by_type(self, type):
        for plugin_name in self.plugins:
            if type in self.plugins[plugin_name]["types"]:
                return self.plugins[plugin_name]["functions"][self.plugins[plugin_name]["types"].index(type)]

    def handle_message(self, message):
        message = json.loads(message)
        function = self.find_plugin_by_type(message["type"])
        return function(message["data"])
