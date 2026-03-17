from qrisp import QuantumFloat

# Create two 4-qubit quantum floats
a = QuantumFloat(2)
b = QuantumFloat(2)

# Initialize values
a[:] = 3
b[:] = 2

# Quantum addition
c = a + b

# Measure the result
print(c.get_measurement())  # Expected: {8.0: 1.0}