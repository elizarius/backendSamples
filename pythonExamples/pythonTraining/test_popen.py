#!/usr/bin/env python
import subprocess

def test_cmd(cmd_one, cmd_two):
    p_one = subprocess.Popen(cmd_one,
                             stdout=subprocess.PIPE)
    p_two = subprocess.Popen(cmd_two,
                             stdin=p_one.stdout,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    out, err = p_two.communicate()
    out = out.decode('utf-8')
    print("out: {}".format(out))
    print("err: {}".format(err))
    print("RC: {}".format(p_two.returncode))

cmd1 = ["ls", "-al", "folderdontexist"]
cmd2 = cmd1[0:2]


my_cmd = ["git", "log", "--pretty=oneline"]
cmd3 = ["grep", "test"]
cmd4 = ["grep"]

test_cmd(cmd1, cmd3)

