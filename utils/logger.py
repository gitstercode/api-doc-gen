import logging
from logging import FileHandler, Formatter
from datetime import datetime

import traceback
import sys
import os

from status_codes import status_codes

# from setup import SITE_PACKAGES

log_path = '/usr/local/bin/docgen_src/docgen.log'

class CustomFormatter(Formatter):
    def __init__(self):
        super(CustomFormatter, self).__init__()

    def format(self, record):
        date_string = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        app_id = "Docgen"
        level = record.levelname
        message = record.msg
        log_messeage = "[%s] APPID=%s TYPE=%s MESSAGE=%s" % (
            date_string, app_id, level, message)

        return log_messeage

def message_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    traces = ''.join(line for line in lines)
    return traces

logger = logging.getLogger(__name__)

# To create an empty log file
# with open(log_path, 'a'):
#     os.utime(log_path, None)

if not os.path.exists(log_path):
    try:
        open(log_path, 'a').close()
    except IOError:
        raise Exception(status_codes.get("612"))

handler = FileHandler(log_path)
handler.setLevel(logging.INFO)
formatter = CustomFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)