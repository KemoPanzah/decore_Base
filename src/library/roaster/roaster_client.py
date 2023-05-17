#TODO - alle hostnames in host_addr umbenennen und überprüfen ob IP eingegeben wurde - auch in Frontend IP Field und Validierung auf IP
from .roaster_functions import Roaster_functions

from paramiko import *
from sshtunnel import SSHTunnelForwarder
import os, inspect, Pyro5.api, time, sys
from pathlib import Path

class Roaster_client(object):
    def __init__(self):
        self.ssh_connection = SSHClient()
        self.ssh_tunnel = None
        self.sftp_connection:SFTPClient = None
        self.init_proxy:Pyro5.api.Proxy = None
        self.roaster_ready = False
        self.roaster_direct = False
    
    def get_functions(self):
        if self.roaster_ready == True and self.roaster_direct == True:
            return Roaster_functions(sftp_connection=None, proxy=None, direct=True)
        elif self.roaster_ready == True and self.roaster_direct == False:
            return Roaster_functions(self.sftp_connection, self.get_new_proxy(), direct=False)
        else:
            return False

    def get_new_proxy(self):
        try:
            t_uri = 'PYRO:Roaster_server@127.0.0.1:' + str(self.ssh_tunnel.local_bind_port)
        except Exception as error:
            print ('get_new_proxy [ERROR] >> ' + str(error))
        else:
            return Pyro5.api.Proxy(t_uri)
    
    def prepare(self, p_host_addr=None, port=None, username=None, password=None):
        
        if p_host_addr == '127.0.0.1':
            self.roaster_direct = True
        else: 
            self.roaster_direct = False
            try:
                self.ssh_connection.set_missing_host_key_policy(AutoAddPolicy())
                self.ssh_connection.connect(p_host_addr, port=port, username=username, password=password)
                self.ssh_tunnel = SSHTunnelForwarder(ssh_address_or_host=p_host_addr, ssh_username='root', ssh_password=password, remote_bind_address=(p_host_addr, 666))
                self.ssh_tunnel.start()
                self.sftp_connection = self.ssh_connection.open_sftp()
            except Exception as error:
                print(error)
                return str(error)
            else:
                self.init_proxy = self.get_new_proxy()
                if self.init_proxy._pyroConnection == None:
                    self.init_proxy  = self.__deploy_pyro(p_host_addr)
                    pass
                if self.is_hot() == True:
                    self.init_proxy.clean_orphan_servers()
                    return True
                else:
                    return False

    def __deploy_pyro(self, p_host_addr):
        t_source = os.path.join(os.path.dirname(inspect.getmodule(self).__file__), 'roaster_server.py')
        t_dest = '/roaster_server.py'
        self.sftp_connection.put(t_source, t_dest)
        t_command = 'python3.9 /roaster_server.py --host "' + p_host_addr + '"' + ' --port 666'
        self.ssh_connection.exec_command(t_command)
        time.sleep(1)
        t_uri = 'PYRO:Roaster_server@127.0.0.1:' + str(self.ssh_tunnel.local_bind_port)
        return Pyro5.api.Proxy(t_uri)

    def is_hot(self):
        if self.roaster_direct == True:
            self.roaster_ready = True
            return True
        elif self.__is_ssh_connected() == True and self.__is_pyro_deployed() == True:
            self.roaster_ready = True
            return True
        else:
            self.roaster_ready = False
            return False

    def __is_ssh_connected(self):
        t_transport = self.ssh_connection.get_transport()
        if t_transport != None and t_transport.is_active() == True:
            return True
        else:
            return False
    
    def __is_pyro_deployed(self):
        try:
            if not self.init_proxy.is_alive() == True:
                print ('[ERROR] >> Roaster_server not alive')
                return False
            elif not self.init_proxy.is_same_python(sys.version_info) == True:
                print ('[ERROR] >> Roaster_server not same python version')
                return False
            else:
                return True
        except Exception as error:
            return False