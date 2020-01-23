"""Container module to manage container operations"""

import subprocess
import sys
import json

from docgen_src.utils.logger import logger, message_traceback
from docgen_src.utils.status_codes import status_codes
from docgen_src.utils.custom_exception import DockerException

class Container(object):
    """
    Container class to manage containers
    """
    _cmd = ""
    _id = None
    _port = None
    _volumes = None
    _base_image = None

    def __init__(self, container_id=None):
        self._id = None
        if container_id:
            cmd_string = "docker inspect --format='{{json .State.Running}}' %s" % (container_id)
            running_status, err = self._exec(cmd_string)
            if running_status:
                self._id = container_id

    def set_port(self, value):
        Container._port = value

    def get_port(self):
        return Container._port

    def set_volume(self, *volumes):
        volume_str = ""
        for volume in volumes:
            if volume is not None:
                volume_str += "-v " + volume + " "
        Container._volumes = volume_str

    def get_volume(self):
        return Container._volumes

    def set_cmd(self, value):
        Container._cmd = value

    def get_cmd(self):
        return Container._cmd

    def set_image(self, value):
        Container._base_image = value

    def get_image(self):
        return Container._base_image

    def start(self):
        """
        Create and start a container.
        :return: tuple of container_id, error, container port.
        """
        if self._id:
            self.remove()

        if self.get_port() is None:
            port = "-P --publish-all"
        else:
            port = "-p %s"%(Container._port)

        cmd_string = "docker create %s %s %s " % (port, self.get_volume(), self.get_image())
        id, err = self._exec(cmd_string)
        id = id.strip()
        self._id = id
        if id:
            cmd_string = "docker start %s" % id
            c_id, err = self._exec(cmd_string)
            c_id = c_id.strip()

            port_running = ""
            if c_id:
                cmd_string = "docker inspect --format='{{json .NetworkSettings.Ports}}' %s" % c_id
                out, err = self._exec(cmd_string)

                if out:
                    out = json.loads(out)
                    port_running = out.get("443/tcp")[0].get("HostPort")
            return c_id, err, port_running

    def stop(self):
        """
        To stop a running container
        :return: Boolean
        """
        if self._id:
            response = False
            cmd_string = "docker stop %s" % self._id
            out, err = self._exec(cmd_string)
            out = out.strip()
            if out:
                response = True
            return response

    def remove(self):
        """To remove a container
        :return: container id"""
        if self._id:
            cmd_string = "docker rm -f %s" % self._id
            out, err = self._exec(cmd_string)
            out=out.strip()
            return out

    def is_running(self):
        """
        To check if container is running.
        :return: Boolean
        """
        container_id = None
        if self._id:
            container_id = self._id
        response = False
        cmd_string = "docker inspect --format='{{json .State}}' %s" % (container_id)
        out, err = self._exec(cmd_string)
        out = out.strip()
        if out:
            out = json.loads(out)
            try:
                running_status = out.get("Running")
                if running_status:
                    response = True
            except Exception, e:
                logger.exception(message_traceback())
                raise Exception("602")
        return response

    def log(self):
        """
        Serves log command for clients
        :return: void
        """
        try:
            container_id = None
            if self._id:
                container_id = self._id
            cmd_string = "docker exec %s %s"%(container_id, self.get_cmd())
            exec_command = subprocess.Popen(cmd_string, shell=True)
            exec_command.wait()

            if exec_command.returncode != 0:
                raise Exception("601")
            return

        except Exception, e:
            logger.exception(e)
            raise

    def execute(self):
        """
        To execute anything on running container if container id exists.
        OR create. execute and remove an ananymous container if container id doesn't exists
        :return: tuple of output and error of command executed
        """
        if not Container.is_docker_running():
            raise Exception("601")

        if self._id:
            cmd_string = "docker exec -d %s %s"%(self._id, self.get_cmd())
            out, err = self._exec(cmd_string)
            out = out.strip()
        else:
            if not Container.is_image_exists(self.get_image()):
                raise Exception("603")
            cmd_string = "docker run --rm %s %s %s" % (self.get_volume(), self.get_image(), self.get_cmd())
            out, err = self._exec(cmd_string)


        return out, err


    def _exec(self,cmd_string):
        """
        To execute docker commands.
        :param cmd_string:
        :return: tuple of output and error of executed command
        """
        if not Container.is_docker_running():
            raise Exception("601")
        if self.get_image():
            if not Container.is_image_exists(self.get_image()):
                raise Exception("603")

        exec_command = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = exec_command.communicate()

        if exec_command.returncode == 125:
            logger.error(err)
            raise Exception("602")
        elif exec_command.returncode != 0:
            logger.error(err)
        return out, err

    @staticmethod
    def is_image_exists(image_name):
        """Check if docker image exists
        :return: Boolean"""
        response = False
        image_check_cmd = subprocess.Popen("docker images -q %s" % image_name, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        out, err = image_check_cmd.communicate()
        if out:
            response = True
        return response

    @staticmethod
    def is_docker_running():
        """
        Check if docker running
        :return: Boolean
        """
        exec_command = subprocess.Popen("docker ps", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        d_out, d_err = exec_command.communicate()
        response = True
        if d_err:
            response = False
        return response

    @staticmethod
    def cleanup():
        pass