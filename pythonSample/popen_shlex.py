#!/usr/bin/env python
import subprocess
import shlex

def test_cmd(cmd1 , cmd2=None):

    print("command: {} |{}".format(cmd1, cmd2))

#    if '|' in cmd:
#        print ('AELZ  pipe found')
#        return
#    w1 = cmd1.split(" ")
#    w2= cmd2.split(" ")


    p_one = subprocess.Popen(cmd1,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p_one.communicate()

#    p_two = subprocess.Popen(w2,
#                            stdin=p_one.stdout,
#                            stdout=subprocess.PIPE,
#                            stderr=subprocess.PIPE)
#    out, err = p_two.communicate()

#    out = out.decode('utf-8')
    print("out: \n{}".format(out))

    print("err: {}".format(err))
    print("RC: {}".format(p_one.returncode))


cmd = "ls -la | grep str"
lexer = shlex.split(cmd)
#lexer.quotes = '|'
#zz = list(lexer)
print("parsed command: {}".format(lexer))

test_cmd(lexer)
#test_cmd("ls -la | grep str")
#test_cmd("ls -al")

