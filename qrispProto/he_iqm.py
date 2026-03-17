from qrisp import *
from qrisp.interface import IQMBackend

api_token = "Po4lmuW24UMMW3lzyZkxqBgu1ObJ8/dvB19e/gYxdpsBnJ8Wc5pwkr5u16eHh3S1"
device_instance = "sirius"

quantum_computer = IQMBackend(
    api_token = api_token,
    device_instance = device_instance)

a = QuantumFloat(2)
a[:] = 2
b = a + a
print("****** AELZ_01 my first qrisp program ******")
a = b.get_measurement(backend = quantum_computer)
print (a)