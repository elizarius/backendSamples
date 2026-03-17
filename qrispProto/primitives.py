from qrisp import QuantumFloat,QuantumBool,  x 

def Xgate(): 

    ### X gate example

    # Create a qubit (initialized to |0>)
    q = QuantumBool()
    print("Boolean Before X gate:", q.get_measurement())  # {False: 1.0}

    # Apply X gate (flips |0> to |1>)
    x(q)
    print("Boolean After X gate:", q.get_measurement())   # {True: 1.0}


    print("\n  **Floating  4 gubits") # {0.0: 1.0}

    q = QuantumFloat(4)
    print("Before:", q.get_measurement())  # {0.0: 1.0}

    # Flip the first qubit (least significant bit)
    x(q[0])
    print("After x(q[0]):", q.get_measurement())  # {1.0: 1.0}
    # print(q.qs, "\n")

    # Flip second qubit
    x(q[1])
    print("After x(q[1]):", q.get_measurement())  # {3.0: 1.0}  (1+2=3)

    # # Flip all variable
    x(q)
    print("After x(q):", q.get_measurement(), "\n")  # {12: 1.0}  

    # print(q.qs, "\n")

print("****** X gate example ******\n")
Xgate()