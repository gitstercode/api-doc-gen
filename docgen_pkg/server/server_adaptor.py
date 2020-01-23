# from docgen.server.server_interface import ServerInterface
from docgen_src.docgen_pkg.server.server_interface import ServerInterface


# class ServerAdaptor(implements(ServerInterface)):
class ServerAdaptor(ServerInterface):

    _supported_languages = {"swagger": ["php"]}
    _name = ""
    _version = ""
    _port = ""
    _config= ""

    def __init__(self, obj):
        self._instance = obj

    @staticmethod
    def get_language_supported():
        return ServerAdaptor._supported_languages

    def start(self):
        return self._instance.start()

    def stop(self):
        return self._instance.stop()

    def is_running(self):
        return self._instance.is_running()

    def set_port(self, port):
        self._instance.set_port(port)

    def get_port(self):
        return self._instance.get_port()

    def set_mount_volumes(self, mount_paths):
        self._instance.set_mount_volumes(mount_paths)

    def get_mount_volumes(self):
        return self._instance.get_mount_volumes()

    def set_filename(self, filename):
        self._instance.set_filename(filename)

    def get_filename(self):
        return self._instance.get_filename()

    def set_config(self, config):
        self._instance.set_config(config)

    def get_config(self):
        return self._instance.get_config()

    def json(self):
        return self._instance.json()

    def log(self):
        return self._instance.log()

    @staticmethod
    def execute(cmd_string):
        pass