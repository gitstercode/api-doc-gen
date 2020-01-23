import unittest
import subprocess
import os
import timeit


class CommandLineTestCase(unittest.TestCase):
    curDir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))  # this will return current directory in which python file resides.
    parentDir = os.path.abspath(os.path.join(curDir, os.pardir))
    _sample_dir = os.path.join("sample")

    def setUp(self):
        print("\n %s"%self._testMethodName)

    def test_stop_before_start(self):
        args = """docgen stop"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertTrue(out.startswith("Server stoppe") or out.startswith("No server is running"))

    def test_start_dir(self):
        args = """docgen start -d %s""" % CommandLineTestCase._sample_dir
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        response = False
        if "Server started on" in out:
            response = True
        self.assertTrue(response)

    def test_start_port_dir(self):
        args = """docgen start -d %s -p 9028""" % CommandLineTestCase._sample_dir
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        response = False
        if "Server started on" in out:
            response = True
        self.assertTrue(response)

    def test_status(self):
        args = """docgen status"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        response = False
        if ("Server not run" in out) or ("Server running at" in out):
            response = True
        self.assertTrue(response)

    def test_stop(self):
        args = """docgen stop"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)

        response = False
        if ("Server stopped" in out) or ("No server is running" in out):
            response = True
        self.assertTrue(response)

    def test_json_with_output(self):
        args = """docgen json -d %s -o swagger.json""" % CommandLineTestCase._sample_dir
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        out = out.split("\n")[-2]
        self.assertTrue(out.startswith("JSON File generated"))

    def test_json_stdout(self):
        args = """docgen json -d %s""" % CommandLineTestCase._sample_dir
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        response = False
        if out:
            response = True
        self.assertTrue(response)

    ###
    ##
    # Parser Tests
    ##
    ###

    def test_parser_command(self):
        args = """docgen"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 0)

    def test_parser_help(self):
        args = """docgen -h"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 0)

    def test_parser_version(self):
        args = """docgen -v"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 0)

    def test_parser_invalid_command(self):
        args = """docgen invalidcommand"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    def test_parser_commands_help(self):
        args = """docgen start -h"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 0)

    def test_parser_commands_help_inbetween(self):
        args = """docgen start -d asdfasd -p 9000 -h"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 0)

    def test_parser_stop(self):
        args = """docgen stop"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 0)

    def test_parser_stop_withoutarg(self):
        args = """docgen stop -d asdfadsf"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    def test_parser_status(self):
        args = """docgen status"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 0)

    def test_parser_status_withoutarg(self):
        args = """docgen status asdfas"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    def test_parser_start_no_option(self):
        args = """docgen start"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    def test_parser_start_missing_req_option(self):
        args = """docgen start -p 7000"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    def test_parser_start_missing_argument(self):
        args = """docgen start -d"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    def test_parser_start_invalid_option(self):
        args = """docgen start -t"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    def test_parser_start_missing_invalid_option(self):
        args = """docgen start -d -t"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    def test_parser_start_valid_invalid(self):
        args = """docgen start -d asdfa -p"""
        out, err, r_code = CommandLineTestCase.exec_out_err(args)
        self.assertEqual(r_code, 1)

    @staticmethod
    def get_returncode(cmd_string):
        exec_command = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exec_command.wait()
        return_code = exec_command.returncode
        return return_code

    @staticmethod
    def exec_out_err(cmd_string):
        exec_command = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = exec_command.communicate()
            r_code = exec_command.returncode
            # print "**********************************"
            # print cmd_string
            # print "out"
            # print out
            # print "err"
            # print err
            # print "returncode"
            # print r_code
            # print "**********************************"
            return out, err, r_code
        except Exception,e:
            print(e)



if __name__ == "__main__":
    unittest.main()