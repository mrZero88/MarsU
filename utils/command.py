import os
import subprocess


class Command:

    @staticmethod
    def run_command(command):
        return subprocess.call(command.split(), stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)

    @staticmethod
    def run_command_with_output_pipe(command):
        output = subprocess.run(command.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return output

    @staticmethod
    def run_command_with_output(command):
        output = subprocess.getstatusoutput(command.split())
        return output[1]

    @staticmethod
    def run_command_with_output_nosplit(command):
        output = subprocess.getstatusoutput(command)
        return output[1]
