"""Server Interface to be used by adaptees and server_adaptor"""

import abc

class ServerInterface(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        return

    @abc.abstractmethod
    def stop(self):
        return

    @abc.abstractmethod
    def is_running(self):
        return

    @abc.abstractmethod
    def set_port(self, port):
        return

    @abc.abstractmethod
    def get_port(self):
        return

    @abc.abstractmethod
    def set_mount_volumes(self, mount_paths):
        return

    @abc.abstractmethod
    def get_mount_volumes(self):
        return

    @abc.abstractmethod
    def set_filename(self, filename):
        return

    @abc.abstractmethod
    def get_filename(self):
        return

    @abc.abstractmethod
    def set_config(self, config):
        return

    @abc.abstractmethod
    def get_config(self):
        return

    @abc.abstractmethod
    def log(self):
        return

    @abc.abstractmethod
    def execute(cmd_string):
        return