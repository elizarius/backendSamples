def foo() :
    "documentation of function foo"
    print "hello from foo"

def bar() :
    """multiline comment starts here
    and continues forever or at least
    to this next line where I terminate it
    but not yet just in the following line
    the termination is finally here"""
    print "fii"
    print "bar"

print foo.__doc__
print bar.__doc__
bar()
