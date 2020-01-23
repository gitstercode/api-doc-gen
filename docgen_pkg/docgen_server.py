import sys

# from docgen_pkg.server.server_adaptor import ServerAdaptor
from docgen_src.docgen_pkg.server.server_adaptor import ServerAdaptor
# from utils.logger import logger, message_traceback
from docgen_src.utils.logger import logger, message_traceback

_SOURCE_PACKAGE = "docgen_src"
_APP_PACKAGE = "docgen_pkg"
_ADAPTEE_PACKAGE = "adaptee"


class DocgenServer(object):
    _update_url = "https://"

    def __init__(self, config):
        if config is None:
            self._config = {}
        else:
            self._config = config

        try:
            self._vendor = self._config.get("vendor")
            self._language = self._config.get("language")

            self._server = None
            if self._language in ServerAdaptor.get_language_supported().get(self._vendor):
                module_name = self._vendor + "_" + self._language
                class_name = self._vendor.capitalize() + self._language.capitalize()
                module = __import__('%s.%s.%s.%s' % (_SOURCE_PACKAGE, _APP_PACKAGE, _ADAPTEE_PACKAGE, module_name), fromlist=[class_name])
                server_adaptor = getattr(module, class_name)
                server_adapter_instance = server_adaptor(self._config)
                self._server = ServerAdaptor(server_adapter_instance)
            else:
                print("Given language and vendor are not supported")
                sys.exit(1)

        except Exception, e:
            logger.exception(message_traceback())
            raise Exception("602")


    def get_vendor(self):
        return self._vendor

    def get_language(self):
        return self._language

    def update(self):
        print("Update not yet configured")

    # Methods for Intercepting Server_adapter
    def __getattr__(self, attr):
        try:
            return super(DocgenServer, self).__getattr__(attr)
        except AttributeError:
            return self.__get_global_handler(attr)

    def __get_global_handler(self, name):
        # Do anything that you need to do before simulating the method call
        handler = self.__global_handler
        handler.im_func.func_name = name
        return handler

    def __global_handler(self, *args, **kwargs):
        # Do something with these arguments
        try:
            func = getattr(self._server, self.__global_handler.im_func.func_name)

            if args:
                response = func(args)
            else:
                response = func()
            return response
        except AttributeError:
            print("%s not found" % self.__global_handler.im_func.func_name)