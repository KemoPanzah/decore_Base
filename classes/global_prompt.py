from argparse import ArgumentParser

class Global_prompt(object):
    def __init__(self):
        self.parser = ArgumentParser()
        self.cmd = self.parser.add_subparsers(dest='cmd')
        self.init = self.cmd.add_parser('prepare', help='Preparation of the decore application.')
        self.create = self.cmd.add_parser('create', help='create')
        self.create.add_argument('-t', '--type', type=str, choices=['base', 'model'], required=True, help='choose your type')
        self.create.add_argument('-i', '--id', type=str, required=True)
        self.create.add_argument('-p', '--parent', type=str, required=False)
        self.args = self.parser.parse_args()
        
        if self.args.cmd == 'prepare': 
            self.prepare()

    def prepare(self):
        pass