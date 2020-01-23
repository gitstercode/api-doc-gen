""""Docker module to perform various docker operations"""
import subprocess


class Docker(object):
    """Docker class to perform various operations like
    --loading image
    --create container
    --destroy container
    --remove all containers"""
    def __init__(self, image_id):
        self._image_id = image_id

    def remove(self):
        """Remove Docker image
        :return Boolean"""
        cmd_string = "docker rmi %s" % (self.get_image_id())
        exec_command = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = exec_command.communicate()
        out = out.strip()
        print(out)
        response = False
        if out:
            response = True
        return response

    def get_image_id(self):
        return self._image_id

    def create_container(self):
        pass

    def remove_container(self):
        """Remove all containers associated with image_id
        :returns Boolean"""
        cmd_string = "docker rm $(docker stop $(docker ps -a -q --filter ancestor=%s --format='{{.ID}}'))" % (self.get_image_id())
        exec_command = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = exec_command.communicate()
        out=out.strip()

        response = False
        if out:
            response = True
        return response

    @staticmethod
    def install(image_file):
        """Loads docker image from tar file
        :return: void
        """
        cmd_string = "docker load -i %s" %image_file
        exec_command = subprocess.Popen(cmd_string, shell=True) #stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exec_command.wait()
        return

    @staticmethod
    def cleanup():
        pass