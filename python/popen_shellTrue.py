#!/usr/bin/env python
import subprocess

def test_cmd(cmd):

    print("command: {}".format(cmd))
    p_two = subprocess.Popen(cmd,
                            shell=True,  
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    out, err = p_two.communicate()
    
    #out = out.decode('utf-8')
    print("out: {}".format(out))
    print("err: {}".format(err))
    print("RC: {}".format(p_two.returncode))

cmd2 = "ls -al | grep stri "
cmd3 = ["ls","-al","|","grep","stri"]
#test_cmd(cmd2)
test_cmd(cmd3)
