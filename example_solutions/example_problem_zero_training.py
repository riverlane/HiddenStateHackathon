from .helper_functions import compute_parity_exp_value, infererance_retval, print_circuit
from qiskit import QuantumCircuit, QuantumRegister, BasicAer, execute

def example_problem_zero_training(training_data):
    # we ignore the training data as we will look at it by hand!
    print("Training data:")
    for training_vec in training_data:
        print("\t{}".format(training_vec))

    num_qubits = 1
    qr = QuantumRegister(num_qubits, "qr")
    circ = QuantumCircuit(qr)

    # you will modify this line as part of the first session of the day.
    # note that H is self-inverse (like a classical NOT): H^-1 == H.
    circ.h(qr[0])

    print("Trying the following circuit:")
    print(print_circuit(circ, num_qubits))

    def infer(wavefunction):

        simulator = BasicAer.get_backend('statevector_simulator')

        opts = {"initial_statevector": wavefunction}
        result = execute(circ, simulator, backend_options=opts).result()
        exp_val = compute_parity_exp_value(result.get_statevector(circ))

        print(exp_val)

        return exp_val

    return infererance_retval(
            infer_fun = infer,
            infer_circ = circ,
            discription = "Circuit generated by hand."
        )
