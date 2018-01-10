import json
from types import FunctionType
import logging

logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self):
        """
        Handles the plugins for managing message data.
        It will use the first plugin registered for the message type.
        """
        self.plugins = {}
        logger.info("Starting plugin manager")

    def register_plugin(self, name: str, types: list, functions: list) -> None:
        """
        Register a new plugin. Index x in 'types' must match index x in 'functions'.
        :param name: Name of the plugin
        :param types: List of strings for the types of messages this plugin handles
        :param functions: List of functions corresponding to the types in the previous lists
        """
        assert (len(types) == len(functions))
        self.plugins[name] = {}
        self.plugins[name]["types"] = types
        self.plugins[name]["functions"] = functions
        logger.info(f"Plugin named '{name}' with types: {types} and functions: {functions} registered.")

    def deregister_plugin(self, name: str) -> bool:
        """
        Deregister a plugin.
        :param name: Plugin to remove
        :return: Deregistration was successful.
        """
        if self.plugins.pop(name, None) is not None:
            logger.info(f"Plugin named '{name}' deregistered")
            return True
        else:
            logger.warn(f"Plugin named '{name}' not found. Deregistration unsuccessful")
            return False

    def find_plugin_by_type(self, type: str) -> FunctionType:
        """
        Find the first plugin function matching the requested type.
        :param type: Type to search for
        :return: The function handling the requested type, if it exists.
        """
        for plugin_name in self.plugins:
            if type in self.plugins[plugin_name]["types"]:
                logger.info(f"Found plugin named '{plugin_name}' to handle type {type}")
                return self.plugins[plugin_name]["functions"][self.plugins[plugin_name]["types"].index(type)]

    def handle_message(self, message: str) -> object:
        """
        Process a message using the appropriate plugin
        :param message: Json string containing the message to be processed
        :return: Response from message processing.
        """
        logger.info(f"Processing message with content '{message}'")
        message = json.loads(message)
        plugin_function = self.find_plugin_by_type(message["header"]["type"])
        response = plugin_function(message["body"])
        logger.info(f"Return message has content '{response}'")
        return response
