#include <Python.h>

//
// Function to be called from Python
// Don't assume any arguments, just return the string
//
static PyObject* py_myFunction(PyObject* self, PyObject* args)
{
	char *s = "Hello from C!";
	return Py_BuildValue("s", s);
}

//
// Another function to be called from Python
// argument provided by a tuple from which we parse the values
//
static PyObject* py_myOtherFunction(PyObject* self, PyObject* args)
{
	double x, y;
	PyArg_ParseTuple(args, "dd", &x, &y);
	return Py_BuildValue("d", x*y);
}

//
// Bind Python function names to our C functions
//
static PyMethodDef myLibrary_methods[] = {
	{"myFunction", py_myFunction, METH_VARARGS},
	{"myOtherFunction", py_myOtherFunction, METH_VARARGS},
	{NULL, NULL}
};

//
// Python calls this to let us initialize our module
// when calling from myLibrary import *
//
void initmyLibrary()
{
	(void) Py_InitModule("myLibrary", myLibrary_methods);
}
