from decore_base.library.powershell.powershell import PS_command as psc, Ps_process

class Test_powershell:

    process = None
    
    @classmethod
    def setup_class(cls):
        cls.process = Ps_process()

    def test_command(self):
        p_cmd_1 = psc('Get-Variable').cmd('ForEach-Object', block=psc('Write-Output', value='$_.Name'))
        assert p_cmd_1.__cmd__ == 'Get-Variable | ForEach-Object {Write-Output $_.Name}'
        p_cmd_2 = psc('Get-Variable').cmd('Where-Object', block=psc('$_.CPU', gt=10))
        assert p_cmd_2.__cmd__ == 'Get-Variable | Where-Object {$_.CPU -gt 10}'
        p_cmd_3 = psc('Get-Process').cmd('ForEach-Object', block=psc('if', value='($_.CPU -gt 10)', block=psc('Write-Output', value='$_.Name')))
        assert p_cmd_3.__cmd__ == 'Get-Process | ForEach-Object {if ($_.CPU -gt 10) {Write-Output $_.Name}}'