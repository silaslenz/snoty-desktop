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

    def register_plugin(self, name: str, message_types: list, functions: list) -> None:
        """
        Register a new plugin. Index x in 'types' must match index x in 'functions'.
        :param name: Name of the plugin
        :param message_types: List of strings for the types of messages this plugin handles
        :param functions: List of functions corresponding to the types in the previous lists
        """
        assert (len(message_types) == len(functions))
        self.plugins[name] = {}
        self.plugins[name]["types"] = message_types
        self.plugins[name]["functions"] = functions
        logger.info(f"Plugin named '{name}' with message types: {message_types} and functions: {functions} registered.")

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
            logger.warning(f"Plugin named '{name}' not found. Deregistration unsuccessful")
            return False

    def find_plugin_by_type(self, message_type: str) -> FunctionType:
        """
        Find the first plugin function matching the requested type.
        :param message_type: Type to search for
        :return: The function handling the requested type, if it exists.
        """
        for plugin_name in self.plugins:
            if message_type in self.plugins[plugin_name]["types"]:
                logger.info(f"Found plugin named '{plugin_name}' to handle type {message_type}")
                return self.plugins[plugin_name]["functions"][self.plugins[plugin_name]["types"].index(message_type)]
        return None

    def handle_message(self, message: str, socket) -> object:
        """
        Process a message using the appropriate plugin
        :param socket: Socket where the message came from. Should still be open for the response.
        :param message: Json string containing the message to be processed
        :return: Response from message processing.
        """
        logger.info(f"Processing message with content '{message}'")
        message = json.loads(message)
        plugin_function = self.find_plugin_by_type(message["type"])
        if plugin_function is None:
            logger.warning(f"Unsupported type {message['type']}")
        else:
            response = plugin_function(message, socket)
            logger.info(f"Return message has content '{response}'")
            return response
