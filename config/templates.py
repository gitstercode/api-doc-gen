"""This Module provides required templates for docgen for various commands
In most cases, this module is consumed by command line parser."""

def template_no_command(cmd):
    message = "Usage: docgen COMMAND [ARGS]... \nError: No such command \"{}\"".format(cmd)
    return message

def template_missing_option(cmd, option):
    option = '\" \"'.join(option)
    message = "Usage: docgen {} [ARGS]\nError:  Missing option \"{}\"".format(cmd, option)
    return message

def template_missing_argument(cmd, option):
    message = "Usage: docgen {} [ARGS]\nError: \"{}\" option requires an argument".format(cmd, option)
    return message

def template_no_such_option(cmd, option):
    message = "Usage: docgen {} [ARGS]\nError: no such option: \"{}\"".format(cmd, option)
    return message

def template_no_options_supported(cmd):
    message = """Usage: docgen {} [ARGS]\nError:  Given command doesn't support arguments""".format(cmd)
    return message

def template_version(client_version=None, server_version=None, docgen_version=None):
    message = """Docgen client: "{}"\nDocgen server: "{}"\nDocgen: "{}" """.format(client_version, server_version, docgen_version)
    return message

def template_help_menu(commands_json):
    commands = commands_json.keys()
    commands = '\n   '.join(commands)
    message = """
Usage: docgen [-v] [COMMAND] [-h] [ARGS]... 

Options:
  -h, help menu
  -v, version

Commands:
   {}""".format(commands)
    return message

def template_command_help(command, command_help, arg_help):
    if arg_help:
        arg_help = ''.join('\n   {}, {}'.format(key, val) for key, val in arg_help.items())

    if not arg_help:
        message = """
Usage: docgen {} [-h]

Description: {}
""".format(command, command_help)
    else:
        message = """
Usage: docgen {} [-h] [OPTIONS]

Description: {}

Options:
   {}""".format(command, command_help, arg_help[4:])

    return message