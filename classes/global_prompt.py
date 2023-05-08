from argparse import ArgumentParser

class Global_prompt(object):
    def __init__(self):
        self.parser = ArgumentParser()
        self.cmd = self.parser.add_subparsers(dest='cmd')
        self.prepare = self.cmd.add_parser('prepare', help='Prepare decore App to get startet')
        self.dev = self.cmd.add_parser('dev', help='Run decore App in Development mode')
        # self.create = self.cmd.add_parser('create', help='create')
        # self.create.add_argument('-t', '--type', type=str, choices=['base', 'model'], required=True, help='choose your type')
        # self.create.add_argument('-i', '--id', type=str, required=True)
        # self.create.add_argument('-p', '--parent', type=str, required=False)
        self.args = self.parser.parse_args()