from asyncio.subprocess import PIPE
from .return_value import Return_value
import json, subprocess

class Ps_command_line(object):
    def __init__(self):
        self.__cmd__ = ''
    
    #TODO - Scripblock wieder entfernen nur reines Piping alles verschachtelte kommt nun aud Custom Modul
    def cmdlet(self, p_cmd, p_scriptblock=None, **kwargs):
        
        if not self.__cmd__:
            self.__cmd__ += p_cmd
        elif self.__cmd__:
            self.__cmd__ += ' | ' + p_cmd

        for key, value in kwargs.items():
            
            self.__cmd__ += ' -'+key
            
            if type(value) == list:
                for index, value2 in enumerate(value):
                    
                    if '$_.' in value2:
                        value2 = '$_."' + value2.replace('$_.','') + '"'
                    else:
                        value2 = '"' + value2 + '"'

                    if index == 0:
                        self.__cmd__ += ' '+value2
                    elif not index == 0:
                        self.__cmd__ += ', '+value2
            
            elif type(value) == str:
                if '$_.' in value:
                    value = '$_."' + value.replace('$_.','') + '"'
                else:
                        value = '"' + value + '"'
                
                self.__cmd__ += ' '+value

        if p_scriptblock:
            self.__cmd__ += ' { ' + p_scriptblock.__cmd__ + ' } '

        return self

class Ps_direct(object):

    def execute(self, p_command:Ps_command_line, p_depth=1):
        r_value:list = []
        t_command = p_command.__cmd__ + ' | ConvertTo-Json -Depth '+ str(p_depth) +' -WarningAction SilentlyContinue'
        proccess = subprocess.run(["pwsh", "-Command", t_command], shell=True, stdout=PIPE, stderr=PIPE, encoding = 'ISO-8859-1')
        stdout = proccess.stdout
        stderr = proccess.stderr
        if stdout:
            t_value = json.loads(stdout)
            if not isinstance(t_value, list):
                r_value.append(t_value)
            else: 
                r_value = t_value

            return Return_value(True, r_value)
        else:
            return Return_value(False, stderr)

class Ps_invoke(object):
    def __init__(self, p_computer_name):
        self.computer_name = p_computer_name

    def execute(self, p_command:Ps_command_line, p_depth=1):
        r_value:list = []
        t_command = 'Invoke-Command -ComputerName ' + self.computer_name + ' -ScriptBlock { ' + p_command.__cmd__ + ' } -WarningAction SilentlyContinue | ConvertTo-Json -Depth '+ str(p_depth) +' -WarningAction SilentlyContinue'
        proccess = subprocess.run(["pwsh", "-Command", t_command], shell=True, stdout=PIPE, stderr=PIPE)
        stdout = proccess.stdout
        stderr = proccess.stderr
        if stdout:
            t_value = json.loads(stdout)
            if not isinstance(t_value, list):
                r_value.append(t_value)
            else: 
                r_value = t_value

            return Return_value(True, r_value)
        else:
            return Return_value(False, self.computer_name + ' > ' + str(stderr))

# class Ps_direct2(object):
#     def execute(self, p_command:Ps_command_line, p_depth=1):
#         r_value:list = []
#         t_command = p_command.__cmd__ + ' | ConvertTo-Json -Depth '+ str(p_depth) +' -WarningAction SilentlyContinue'
#         proccess = subprocess.Popen(['pwsh.exe', '-Command', r'-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding = 'ISO-8859-1')
#         proccess.stdin.write(t_command)
#         output = proccess.communicate()
#         stdout = output[0]
#         stderr = output[1]
#         if stdout:
#             t_value = json.loads(stdout)
#             if not isinstance(t_value, list):
#                 r_value.append(t_value)
#             else: 
#                 r_value = t_value

#             return Return_value(True, r_value)
#         else:
#             return Return_value(False, stderr)