import dill, base64
from pathlib import Path

#Todo - verlegen in library
class Return_values(object):
    def __init__(self, p_value):
        self.result = None
        self.error = None
        self.set_values(p_value)

    def set_values(self, p_value):
        if type(p_value) == str and '[ERROR]' in p_value:
            self.result = None
            self.error = p_value
            print (self.error)
        else:
            self.result = p_value
            self.error = None

def roast(proxy, direct, *modules):
    def func_wrapper(func):
        def call_wrapper(*args, **kwargs):
            
            if proxy != None and direct == False:
                try:
                    func_code_dump = dill.dumps(func.__code__)
                    if len(modules) > 0: proxy.install_modules(*modules)
                    return_dump = proxy.roast(func_code_dump, *args, **kwargs)
                    r_value = Return_values(dill.loads(base64.b64decode(return_dump['data'])))
                    return r_value
                except Exception as error:
                    return Return_values('roast [ERROR] >> ' + str(error))
            
            if proxy == None and direct == True:
                try:
                    r_value = Return_values(func(*args, **kwargs))
                    return r_value
                except Exception as error:
                    return Return_values('roast [ERROR] >> ' + str(error))

        return call_wrapper
    return func_wrapper

class Roaster_functions(object):
    def __init__(self, sftp_connection=None, proxy=None, direct=None):
        self.sftp_connection = sftp_connection
        self.proxy = proxy
        self.direct = direct
    
    def file_upload(self, p_path:str, p_target_path:str):
        '''Please give me the p_path an p_target_path param .as_posix()'''
        t_path = Path(p_path)
        t_target_path  = Path(p_target_path)
        
        if self.direct == True:
            try:
                import shutil
                shutil.copyfile(t_path, t_target_path)
            except Exception as error:
                return Return_values('file_upload [ERROR] >>' + str(error))
            else:
                return Return_values(True)
        
        if self.direct == False:
            try:
                self.sftp_connection.put(t_path, t_target_path.as_posix(), confirm=True)
            except Exception as error:
                return Return_values('file_upload [ERROR] >>' + str(error))
            else:
                return Return_values(True)
    
    def platform_system(self):
        @roast(self.proxy, self.direct)
        def roast_platform_system():
            r_value = None
            try:
                import platform
                r_value = platform.system()
            except Exception as error:
                return 'platform_system [ERROR] >> ' + str(error)
            else:
                return r_value
        return roast_platform_system()
    
    def path_rm(self, p_path:str):
        '''Please give me the p_path param .as_posix()'''
        @roast(self.proxy, self.direct)
        def roast_path_rm(p_path:str):
            try:
                def remove(f: Path):
                    if f.is_file():
                        f.unlink()
                    else:
                        for child in f.iterdir():
                            remove(child)
                        f.rmdir()
                t_path = Path(p_path)
                remove(t_path)
            except Exception as error:
                return 'path_rm [ERROR] >> ' + str(error)
            else:
                return True
        return roast_path_rm(p_path)

    def path_chmod(self, p_path:str, mode:int):
        '''Please give me the p_path param .as_posix()'''
        @roast(self.proxy, self.direct)
        def roast_path_chmod(p_path:str, mode:int):
            try:
                t_path = Path(p_path)
                t_path.chmod(mode)
            except Exception as error:
                return 'path_chmod [ERROR] >> ' + str(error)
            else:
                return True
        return roast_path_chmod(p_path, mode)

    def path_mkdir(self, p_path:str):
        '''Please give me the p_path param .as_posix()'''
        @roast(self.proxy, self.direct)
        def roast_path_mkdir(p_path:str):
            try:
                t_path = Path(p_path)
                t_path.mkdir(parents=True, exist_ok=True)
            except Exception as error:
                return 'path_mkdir [ERROR] >> ' + str(error)
            else:	
                return True
        return roast_path_mkdir(p_path)

    def path_exists(self, p_path:str):
        '''Please give me the p_path param .as_posix()'''
        @roast(self.proxy, self.direct)
        def roast_path_exists(p_path:str):
            r_value = False
            try:
                t_path = Path(p_path)
                r_value = t_path.exists()
            except Exception as error:
                return 'path_exists [ERROR] >> ' + str(error)
            else:
                return r_value
        return roast_path_exists(p_path)

    def copyfile(self, p_path:str, p_target_path:str):
        '''Please give me the p_path an p_target_path param .as_posix()'''
        @roast(self.proxy, self.direct)
        def roast_copyfile(p_path:str, p_target_path:str):
            try:
                import os, platform
                t_path = Path(p_path)
                t_target_path = Path(p_target_path)

                if platform.system() == 'Windows':
                    t_val = 'xcopy "%s" "%s"* /Y' % (t_path.absolute(), t_target_path.absolute())
                    os.system(t_val)

            except Exception as error:
                return 'copyfile [ERROR] >> ' + str(error)
            else:	
                return True
        return roast_copyfile(p_path, p_target_path)

    def zipfile_unzip(self, p_path:str, p_target_path:str):
        '''Please give me the p_path and p_target_path param .as_posix()'''
        @roast(self.proxy, self.direct)
        def roast_zipfile_unzip(p_path:str, p_target_path:str):
            try:
                t_path = Path(p_path)
                t_target_path = Path(p_target_path)
                from zipfile import ZipFile
                t_zipfile = ZipFile(t_path)
                t_zipfile.extractall(t_target_path)
            except Exception as error:
                return 'zipfile_unzip [ERROR] >> ' + str(error)
            else:
                return True
        return roast_zipfile_unzip(p_path, p_target_path)

    def subprocess_popen(self, p_path:str, *params:str):
        '''Please give me the p_path param .as_posix()'''
        @roast(self.proxy, self.direct)
        def roast_subprocess_popen(p_path:str, *params:str):
            try:
                import subprocess
                t_path = Path(p_path)
                subprocess.Popen([str(t_path), *params])
            except Exception as error:
                return 'process_start [ERROR] >> ' + str(error)
            else:
                return True
        return roast_subprocess_popen(p_path, *params)

    def psutil_process_exists(self, p_process_name:str):
        @roast(self.proxy, self.direct, 'psutil')
        def roast_psutil_process_exists(p_process_name:str):
            r_value = False
            try:
                import psutil
                for proc in psutil.process_iter():
                    if p_process_name.lower() == proc.name().lower():
                        r_value = True
            except Exception as error:
                return 'process_exists [ERROR] >> ' + str(error)
            else:
                return r_value
        return roast_psutil_process_exists(p_process_name)

    def psutil_process_kill(self, p_process_name:str):
        @roast(self.proxy, self.direct, 'psutil')
        def roast_psutil_process_kill(p_process_name:str):
            r_value = False
            try:
                import psutil
                for proc in psutil.process_iter():
                    if p_process_name.lower() == proc.name().lower():
                        proc.kill()
                        #TODO - proc.wait(timeout=5)
                        r_value = True
            except Exception as error:
                return 'psutil_process_kill [ERROR] >> ' + str(error)
            else:
                return r_value
        return roast_psutil_process_kill(p_process_name)

    def pyroute2_ip_exists(self, ip_addr:str):
        @roast(self.proxy, self.direct, 'pyroute2')
        def roast_pyroute2_ip_exists(ip_add:str):
            r_value = False
            try:
                import pyroute2
                t_ipr = pyroute2.IPRoute()
                for addr in  t_ipr.get_addr():
                    if addr.get_attr('IFA_ADDRESS') == ip_add:
                        r_value = True
            except Exception as error:
                return 'pyroute2_ip_exists [ERROR] >> ' + str(error)
            else:
                return r_value
        return roast_pyroute2_ip_exists(ip_addr)

    def pyroute2_get_interface_by_ip(self, ip_addr:str):
        @roast(self.proxy, self.direct, 'pyroute2')
        def roast_pyroute2_get_interface_by_ip(ip_add:str):
            r_value = None
            try:
                import pyroute2
                t_ipr = pyroute2.IPRoute()
                for addr in t_ipr.get_addr():
                    if addr.get_attr('IFA_ADDRESS') == ip_add:
                        t_index = addr['index']
                        for link in t_ipr.get_links():
                            if link['index'] == addr['index']:
                                r_value = link.get_attr('IFLA_IFNAME')
            except Exception as error:
                return 'pyroute2_get_interface_by_ip [ERROR] >> ' + str(error)
            else:
                return r_value
        return roast_pyroute2_get_interface_by_ip(ip_addr)

    def pyroute2_add_ip_by_interface(self, ip_addr:str, sub_mask:int, inf_name:str):
        @roast(self.proxy, self.direct, 'pyroute2')
        def roast_pyroute2_add_ip_by_interface(ip_addr:str, sub_mask:int, if_name:str):
            try:
                import pyroute2
                t_ipr = pyroute2.IPRoute()
                t_index = t_ipr.link_lookup(ifname=if_name)[0]
                t_ipr.addr('add', index=t_index, address=ip_addr, mask=sub_mask)
            except Exception as error:
                return 'pyroute2_add_ip_by_interface [ERROR] >> ' + str(error)
            else: 
                return True
        return roast_pyroute2_add_ip_by_interface(ip_addr, sub_mask, inf_name)

    def pyroute2_delete_ip_by_interface(self, ip_addr:str, sub_mask:int, inf_name:str):
        @roast(self.proxy, self.direct, 'pyroute2')
        def roast_pyroute2_delete_ip_by_interface(ip_addr:str, sub_mask:int, if_name:str):
            try:
                import pyroute2
                t_ipr = pyroute2.IPRoute()
                t_index = t_ipr.link_lookup(ifname=if_name)[0]
                t_ipr.addr('delete', index=t_index, address=ip_addr, mask=sub_mask)
            except Exception as error:
                return 'pyroute2_delete_ip_by_interface [ERROR] >> ' + str(error)
            else: 
                return True
        return roast_pyroute2_delete_ip_by_interface(ip_addr, sub_mask, inf_name)

    def json_request(self, port:int, user:str, password:str, method:str, *params:str):
        @roast(self.proxy, self.direct,'requests')
        def roast_json_request(port:int, user:str, password:str, method:str, *params:str):
            r_value = None
            try:
                import json
                import requests
                t_url = 'http://127.0.0.1:' + str(port)
                t_params:list = []
                for i_param in params: t_params.append(i_param)
                t_data = json.dumps({"method": method, "params": t_params})
                t_headers = {'content-type': "application/json", 'cache-control': "no-cache"}
                response = requests.request("POST", t_url, data=t_data, headers=t_headers, auth=(user, password))
                r_value =  json.loads(response.text)
            except Exception as error:
                return 'json_request [ERROR] >> ' + str(error)
            else:
                return r_value
        return roast_json_request(port, user, password, method, *params)