import codecs

inputfile = codecs.open("ansifile", "r", "latin1")
outputfile = codecs.open("utf8file", "w", "utf8")
data = inputfile.read()
outputfile.write(data)
inputfile.close()
outputfile.close()
