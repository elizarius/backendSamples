from subprocess import Popen

#output = `dir`
output = Popen(["./hello", r"All"])
output.call("func1")
output.communicate()
print "==================================="
print output
