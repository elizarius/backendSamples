#!/usr/bin/env python
import subprocess

def test_cmd(cmd):
#    p_one = subprocess.Popen(cmd_one,
#                             stdout=subprocess.PIPE)

    print("command: {}".format(cmd))

    if '|' in cmd:
        print ('AELZ  pipe found')
        return 

    if '>' in cmd:
        print ('AELZ redirect found')
        return 


    words = cmd.split(" ")
    p_two = subprocess.Popen(words,
                            shell=False,                                                    
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p_two.communicate()
#    out = out.decode('utf-8')
    print("out: {}".format(out))
    print("err: {}".format(err))
    print("RC: {}".format(p_two.returncode))


test_cmd("ls -al |grep str")
test_cmd("ls -al")
test_cmd("ls -al > z.log")

