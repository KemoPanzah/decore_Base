# fmt: off
import sys, os
sys.path.append(os.path.abspath('../../'))
from decore_base import decore
# fmt: on

if 'main' in __name__:
    @decore.app(p_title='Sample App')
    def main():
        pass