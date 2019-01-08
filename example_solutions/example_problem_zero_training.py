from .helper_functions import compute_parity_exp_value
from qiskit import QuantumCircuit, QuantumRegister, BasicAer, execute

def example_problem_zero_training(training_data):
    # we ignore the training data as we will look at it by hand!
    print(training_data)

    def infer(wavefunction):

        simulator = BasicAer.get_backend('statevector_simulator')
        qr = QuantumRegister(1, "qr")
        circ = QuantumCircuit(qr)

        # you will modify this line as part of the first session of the day.
        # note that H is self-inverse (like a classical NOT): H^-1 == H.
        circ.h(qr[0])

        opts = {"initial_statevector": wavefunction}
        result = execute(circ, simulator, backend_options=opts).result()
        exp_val = compute_parity_exp_value(result.get_statevector(circ))

        print(exp_val)

        return exp_val

    return infer