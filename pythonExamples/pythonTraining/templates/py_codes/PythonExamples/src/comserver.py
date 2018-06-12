# comserver.py

import win32com.server.register

class COMCalc:

    _reg_progid_ = 'MyClass.PyCalculator'
    _public_methods_ = ['sum']

    #  DON'T COPY THE CLSID
    # print pythoncom.CreateGuid()  to generate it
    _reg_clsid_ = "{BDAE7B6D-390C-41FF-91DC-968F2DDC45A2}"

    def sum(self, arg1, arg2):
        return arg1 + arg2

if __name__ == '__main__':
    print "Registering!"
    win32com.server.register.UseCommandLine(COMCalc)
    