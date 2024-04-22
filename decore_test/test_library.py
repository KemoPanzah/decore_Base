from decore_base.library.powershell3 import *

class Test_powershell:

    process = None
    
    @classmethod
    def setup_class(cls):
        cls.process = Ps_process()

    def test_command(self):
        p_cmd = PS_command('Get-Variable').cmd('ForEach-Object', block=PS_command('Write-Output', key='Name'))
        t_test_1 = self.process.execute(p_cmd)
        p_cmd = PS_command('Get-Mailbox')
        t_test_2 = self.process.execute(p_cmd)

        assert True