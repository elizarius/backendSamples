#!/usr/bin/env python
import subprocess

def test_cmd(cmd):
    words = cmd.split(" ")
    print("command: {}".format(words))

    p_two = subprocess.Popen(words,
                            shell=False,  
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    out, err = p_two.communicate()
    
    #out = out.decode('utf-8')
    print("out: {}".format(out))
    print("err: {}".format(err))
    print("RC: {}".format(p_two.returncode))

#cm1 = "ls -al"

test_cmd("ls -al")
#test_cmd("dropdb --if-exists aelz")
#test_cmd("ls -al | grep str")

