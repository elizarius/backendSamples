#   AELZ_102 input form command line exercise
#   AELZ_103 only for pytho 2.x , input() to be used for python

print "How old are you?",
age = raw_input()
print "How tall are you?",
height = raw_input()
print "How much do you weigh?",
weight = raw_input()

print "So, you're %s old, %s tall and %s heavy." % (
    age, height, weight)

print "together:  %d" % (int(age) +int (height) + int(weight))


# Compact version (ex12)
# AELZ_103: see exa12 on pydoc help
age = raw_input("How old are you? ")
height = raw_input("How tall are you? ")
weight = raw_input("How much do you weigh? ")

print "So, you're %r old, %r tall and %r heavy." % (
    age, height, weight)
