import json
import os
import shutil
import subprocess
import sys

from docgen_pkg.platform.docker import Docker
from utils.logger import logger, message_traceback

USR_BIN = "/usr/local/bin"
DOCGEN_SRC = "docgen_src"
DOCGEN_CLIENT = "docgen"

SITE_PACKAGES = os.path.join(USR_BIN, DOCGEN_SRC)
DOCGEN_CLIENT_PATH = os.path.join(USR_BIN, DOCGEN_CLIENT)

INIT_CONFIG_FILE = "docgen_config.json"
CONFIG_PATH = "config/%s"%INIT_CONFIG_FILE

IMAGE_FILE="docgen-image.tar.gz"
REQUIREMENTS="requirements"
IMAGE_TAR_PATH = os.path.join(REQUIREMENTS, IMAGE_FILE)

LOG_PATH = os.path.join(SITE_PACKAGES, "docgen.log")

INIT_COMMANDS_PATH = "config/docgen_commands.json"
COMMANDS_JSON_PATH = INIT_COMMANDS_PATH

def util_rm_file_or_folder(path, verbose=False):
    """To remove a file or folder if already exists"""
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
        if verbose:
            print "Removed %s"%path

def install_docgen():
    """
    Installs docgen by removing older images, load new image and copying the source and client to /usr/local/bin/
    :return: void
    """
    old_image = ""
    with open(CONFIG_PATH, 'r') as f:
        json_data = json.load(f)
        old_image = json_data["old_image"]

    ## To remove any running container, or old docgen image before install
    docker = Docker(old_image)
    docker.remove_container()
    docker.remove()

    ## To un-tar docgen-image and then load the image.
    if os.path.exists(IMAGE_TAR_PATH):
        Docker.install(IMAGE_TAR_PATH)

    ## Copies downloaded docgen_src to "/usr/local/bin"
    if not os.path.exists(USR_BIN):
        raise
    cur_dir = os.path.abspath(os.curdir)
    try:
        util_rm_file_or_folder(SITE_PACKAGES)               # Remove if docgen_src already exists
        shutil.copytree(cur_dir, SITE_PACKAGES)             # Copy the current packages to docgen_src in /usr/local/bin/docgen/src

        ## Copies docgen to "/usr/local/bin"
        init_client_path = os.path.join(cur_dir, DOCGEN_CLIENT)
        shutil.copy(init_client_path, USR_BIN)

        ## Change mode for docgen_src and docgen client.
        os.chmod(DOCGEN_CLIENT_PATH, 0777)
        os.chmod(SITE_PACKAGES, 0777)

        if not os.path.exists(LOG_PATH):
            open(LOG_PATH, 'a').close()

        os.chmod(CONFIG_PATH, 0777)
        os.chmod(LOG_PATH, 0777)
        os.chmod(COMMANDS_JSON_PATH, 0777)

    except OSError as e:
        print(e)

    return

def uninstall_docgen():
    """
    Uninstalls docgen from uninstall file and removing docgen-image and containers
    :return: void
    """
    ##To remove docgen-image and any containers
    try:
        new_image = ""
        with open(CONFIG_PATH, 'r') as f:
            json_data = json.load(f)
            new_image = json_data["new_image"]

        docker = Docker(new_image)
        docker.remove_container()
        docker.remove()

        util_rm_file_or_folder(DOCGEN_CLIENT_PATH, verbose=True)
        util_rm_file_or_folder(SITE_PACKAGES, verbose=True)
        print("Docgen is been uninstalled")
        return
    except OSError:
        print("To uninstall docgen completely, Try the same command with sudo (root permissions).")

if __name__ == "__main__":
    option = sys.argv[1].strip(',')
    if option == "install":
        install_docgen()
    elif option == "uninstall":
        uninstall_docgen()
    elif option == "log":
        cmd_exec = subprocess.Popen("docgen", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = cmd_exec.communicate()
        if err:
            print("Please check logs at %s" % LOG_PATH)
            logger.error(err)