from .helper_functions import compute_parity_exp_value
from qiskit import QuantumCircuit, QuantumRegister, BasicAer, execute
import itertools
import numpy as np

def example_general_discrete_problem_training(training_data):
    """The example training function for the users.
    This is for the discrete problems (staring with D), continuous problems
    have a different train function.

    Lots of opportunities exist for speeding this up. We have used this function internally
    to annotate all problems with the expected training time and will report if you beat that
    or not!
    """

    num_qubits = int(np.log2(len(training_data[0][0]))) # the wavefunction has 2**NQ elements.

    # This is not every gate - you may need to extend this.
    # A "gate" is a function that takes the circuit and qreg (created later)
    # We need this as gates are methods on the circuits rather than independent objects in qiskit.
    # FORMAT: lambda qiskit gate specification, string description of gate/qubit
    allowable_gates = \
        [(lambda circ, qreg: circ.h(qreg[i]), "".join(f"H{i}")) for i in range(num_qubits)] + \
        [(lambda circ, qreg: circ.x(qreg[i]), "".join(f"X{i}")) for i in range(num_qubits)] + \
        [(lambda circ, qreg:
          circ.cx(qreg[i], qreg[i+1]), "".join(f"CNOT({i}, {i+1}")) for i in range(num_qubits - 1)]


    print("Gate set:")
    print([gfun[1] for gfun in allowable_gates])

    max_length = num_qubits * 2 # the total number of gates to consider
    print(f"Maximum gate depth {max_length}")

    # NOTE: some gates are not affected by ordering!
    # for example, 2 gates on 2 different qubits can be exchanged.
    # this is not considered here.
    possible_circuits = itertools.chain(*[
                        itertools.permutations((gates[0] for gates in allowable_gates), r=NG)
                        for NG in range(max_length+1)
                       ])
    labelled_combinations = itertools.chain(*[
                        itertools.permutations((gates[1] for gates in allowable_gates), r=NG)
                        for NG in range(max_length+1)
                       ])

    possible_circuits = list(possible_circuits)
    print(f"Number of possible circuits to consider: {len(possible_circuits)}")
    labelled_combinations = list(labelled_combinations)
    print(labelled_combinations)

    # if you want to print all the attempts, this can help:
    # for p in possible_circuits:
    #     print([(str(g), i) for g, i in p])

    best_cost = float('Inf')
    best_circuit = None
    index = 0
    for current_circuit in possible_circuits:
        current_cost = 0
        for train_vector, train_label in training_data:

            simulator = BasicAer.get_backend('statevector_simulator')
            qr = QuantumRegister(num_qubits, "qr")
            circ = QuantumCircuit(qr)

            if len(current_circuit) == 0:
                circ.iden(qr)
            else:
                for gate_application_function in current_circuit:
                    gate_application_function(circ, qr)

            opts = {"initial_statevector": train_vector}
            execution = execute(circ, simulator, backend_options=opts)
            result = execution.result()
            print(f"vector: {result.get_statevector(circ)}")
            prediction = compute_parity_exp_value(result.get_statevector(circ))

            current_cost += abs(train_label - prediction)
            print(f"ground truth: {train_label}")
            print(f"prediction:   {prediction}")
            print(f"difference: {train_label - prediction}")
            print()

        # print(".", end="", flush=True)
        if current_cost < best_cost:
            best_circuit = current_circuit
            best_cost = current_cost
            best_index = index
        # if best_cost == 0.0:
        #     break # done!
        index += 1


    print("done")
    print(f"best circuit: {labelled_combinations[best_index]} with cost {best_cost}")

    # now we create the inference function. This should take a state and produce a prediction.
    def infer(wavefunction):

        simulator = BasicAer.get_backend('statevector_simulator')
        qr = QuantumRegister(num_qubits, "qr")
        circ = QuantumCircuit(qr)

        for gate in best_circuit:
            gate(circ, qr)

        opts = {"initial_statevector": wavefunction}
        result = execute(circ, simulator, backend_options=opts).result()
        result = compute_parity_exp_value(result.get_statevector(circ))

        return result

    return infer
