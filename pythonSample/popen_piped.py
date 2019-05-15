#!/usr/bin/env python
import subprocess

def test_cmd(cmd1 , cmd2=None):

    print("command: {} |{}".format(cmd1, cmd2))

#    if '|' in cmd:
#        print ('AELZ  pipe found')
#        return
#    w1 = cmd1.split(" ")
#    w2= cmd2.split(" ")


    p_one = subprocess.Popen(cmd1,
                            stdout=subprocess.PIPE)
    p = p_one
    if cmd2 is not None:
        p = subprocess.Popen(cmd2,
                                 stdin=p_one.stdout,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

    out, err = p.communicate()
    ret_code = p.returncode
#    out = out.decode('utf-8')
    print("out: \n{}".format(out))
    print("err: {}".format(err))
    print("RC: {}".format(ret_code))

c1 = "ls -la"
c2 = "grep str"
test_cmd(c1.split(' '), c2.split(' '))
#test_cmd("ls -la", "grep str")
test_cmd(c1.split(' '))

