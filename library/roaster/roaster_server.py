import pip, base64, types, subprocess, os, sys
from pathlib import Path

try:
    import Pyro5.api, debugpy, dill, psutil
    debugpy.listen(('0.0.0.0', 5678))
except ImportError:
    pip.main(['install', '-q', 'Pyro5'])
    pip.main(['install', '-q', 'debugpy'])
    pip.main(['install', '-q', 'dill'])
    pip.main(['install', '-q', 'psutil'])
    import Pyro5.api, debugpy, dill, psutil
    debugpy.listen(('0.0.0.0', 5678))

@Pyro5.api.expose
class Roaster_server(object):
    def roast(self, func_code_dump, *args, **kwargs):
        func_code = dill.loads(base64.b64decode(func_code_dump['data']))
        func = types.FunctionType(func_code, globals(), "func")
        r_value = func(*args, **kwargs)
        return dill.dumps(r_value)
    
    def install_modules(self, *modules):
            for module in modules:
                try:
                    r_value = pip.main(['install', '-q', module])
                except Exception as error:
                    return 'install_modules [ERROR] >> ' + str(error)
                else:
                    return str(r_value)
    
    def is_alive(self):
        return True

    def is_same_python(self, version_info):
        if sys.version_info[0] == version_info[0] and sys.version_info[1] == version_info[1]:
            return True
        else: 
            return False

    def clean_orphan_servers(self):
        t_pid = os.getpid()
        for t_process in psutil.process_iter():
            if 'roaster_server.py' in str(t_process.cmdline()): 
                if t_process.pid != t_pid:
                    breakpoint()
                    t_process.kill()
                    pass

def fire_up():
    import argparse, sys
    t_parser = argparse.ArgumentParser(description='Fire up Pyro and start the Roaster')
    t_parser.add_argument('--host', default='127.0.0.1', type=str, help='Host address')
    t_parser.add_argument('--port', default=666, type=int, help='Host port')
    args = t_parser.parse_args()

    daemon = Pyro5.api.Daemon(host=args.host, port=args.port)
    uri = daemon.register(Roaster_server, 'Roaster_server')
    print(uri)
    daemon.requestLoop()

if __name__ == "__main__":
    fire_up()