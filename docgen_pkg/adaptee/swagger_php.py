"""Swagger PHP module to manage commands for swagger php plugin commands in the image."""

from docgen_src.docgen_pkg.platform.container import Container
from docgen_src.docgen_pkg.server.server_interface import ServerInterface
from docgen_src.utils.logger import logger, message_traceback


class SwaggerPhp(ServerInterface):
    """
    This Class manages commands for swagger-php plug-in thats installed in the image.
    Supports various methods required to execute operations on the swagger-php plugin.
    """
    _BASE_IMAGE_NAME = "docgen-image"
    _JSON_APACHE_PATH = "/var/www/html/data/"
    SWAGGER_PHP_CONFIG_FILE = "/Config/bootstrap.php"   ##Rename this variable

    _port = 0
    _mount_volumes = []
    _filename = ""
    _bootstrap = ""
    _config_file = ""

    def __init__(self, _config):
        """Constructor"""
        if _config is None:
            self._config = {}
        else:
            self._config = _config

    def get_base_image(self):
        return self._BASE_IMAGE_NAME

    def start(self):
            response=False

            dir_volume=""
            if self.get_mount_volumes():
                dir_volume=self.get_mount_volumes()[0]
            volume = "%s:/Apps"%dir_volume

            port = None
            if self.get_port():
                port = "%s:443" % (self.get_port())

            if self.get_filename():
                controller="/Apps/%s" %self.get_filename()
            else:
                controller="/Apps/"

            controller_config_params = ""
            controller_config_volume = self._config.get("bootstrap")
            if controller_config_volume:
                controller_config_volume = "%s:%s" %(controller_config_volume, SwaggerPhp.SWAGGER_PHP_CONFIG_FILE)
                controller_config_params = "--bootstrap %s" %SwaggerPhp.SWAGGER_PHP_CONFIG_FILE
            else:
                controller_config_volume = None

            container = Container(self.get_config().get("id"))
            container.set_volume(volume,
                                 controller_config_volume
                                 )
            container.set_port(port)
            container.set_image(SwaggerPhp._BASE_IMAGE_NAME)
            id, err, port_running = container.start()
            self._config["id"] = id
            self._config["port"] = port_running
            if id:
                response = True
                exec_params =  "/startup.sh" + " " + controller + " " + "--output" + " " + SwaggerPhp._JSON_APACHE_PATH + " " + controller_config_params  #' '.join(exec_params)
                container.set_cmd(exec_params)
                container.execute()

            return response


    def stop(self):
        try:
            c_id = self.get_config().get("id")
            if id:
                response = False
                container = Container(c_id)
                if container.stop():
                    response = True
                    container.remove()
                return response
        except Exception, e:
            logger.exception(message_traceback())
            raise Exception("602")

    def is_running(self):
        container_id = self.get_config().get("id")
        container = Container(container_id)
        response = container.is_running()
        return response

    def set_port(self, port):
        SwaggerPhp._port=port

    def get_port(self):
        return SwaggerPhp._port

    def set_mount_volumes(self, mount_paths):
        SwaggerPhp._mount_volumes = mount_paths

    def get_mount_volumes(self):
        return SwaggerPhp._mount_volumes

    def set_filename(self, filename):
        SwaggerPhp._filename = filename

    def get_filename(self):
        return SwaggerPhp._filename

    def set_controller_config(self, config):
        SwaggerPhp._config_file = config

    def get_controller_config(self):
        return SwaggerPhp._config_file

    def set_config(self, config):
        pass

    def get_config(self):
        return self._config

    def json(self):
        dir_volume = ""
        if self.get_mount_volumes():
            dir_volume = self.get_mount_volumes()[0]
        volume = "%s:/Apps" % dir_volume

        if self.get_filename():
            controller="/Apps/%s" %self.get_filename()
        else:
            controller="/Apps/"

        controller_config_params = ""
        controller_config_volume = self._config.get("bootstrap")
        if controller_config_volume:
            controller_config_volume = "%s:%s" % (controller_config_volume, SwaggerPhp.SWAGGER_PHP_CONFIG_FILE)
            controller_config_params = "--bootstrap %s" % SwaggerPhp.SWAGGER_PHP_CONFIG_FILE
        else:
            controller_config_volume = None

        cmd = "/ngs/app/data/swagger-php/vendor/bin/swagger %s %s --stdout"%(controller, controller_config_params)

        container = Container()
        container.set_volume(volume, controller_config_volume)
        container.set_image(SwaggerPhp._BASE_IMAGE_NAME)
        container.set_cmd(cmd)
        out, err = container.execute()

        err = err[:err.rfind('\n')]
        err = err[:err.rfind('\n')]
        err = err[:err.rfind('\n')]

        response = [out, err]
        return response

    def log(self):
        try:
            container = Container(self.get_config().get("id"))
            cmd_log = "tail -f /Logs/swagger.log"
            container.set_cmd(cmd_log)
            container.log()
        except Exception, e:
            logger.exception(message_traceback())
            raise Exception("602")

        except KeyboardInterrupt:
            print("  Aborted!")

    @staticmethod
    def execute(cmd_string):
        pass