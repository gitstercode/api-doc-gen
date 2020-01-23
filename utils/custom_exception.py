class DockerException(Exception):
    def __init__(self, errorcode):
        super(DockerException, self).__init__(errorcode)

class CommandException(Exception):
    def __init__(self, errorcode):
        super(CommandException)

class CommonException(Exception):
    def __init__(self, errorcode):
        super(CommonException, self).__init__(errorcode)