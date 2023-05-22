# fmt: off
import sys, os
sys.path.append(os.path.abspath('../../'))
from decore_base import decore
# fmt: on

if __name__ == '__main__':
    @decore.app(p_title='Decore Sample Application')
    def main():
        pass