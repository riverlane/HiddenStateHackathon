# Paris Quantum Hackathon

The challenge is to create quantum circuits to classify a provided basket of states into of the Schroedinger's cat classes: ALIVE or DEAD.

tools in this repo include
- example_solutions.py, inefficient example solutions for the problems we set.
- problem_spec_script.py, a tool for creating the problem sets
- evaluate.py, a tool for grading your solutions on accuracy and time.

### Installation

```
git clone git@github.com:riverlane/paris.git
pip install --user projectq sklearn
```

### Usage

Read through the first and second parts of example_solutions.py. In the first session of the day we will prepare your computers and walk through problem D0. The first function `problemzero_example_train` is related to this.

Next you will be free to attempt the discrete and continuous problem sets. We recommend starting with the `train_discrete_general_example` and `TODO` functions.

In order to test your solutions, use `evaluate.py`. A example use is `./evaluate.py --fun train_discrete_general_example --stats --problem problem1 --n 4`. This runs your function `train_discrete_general_example` on problem 1, using 4 vectors for the training set.

If you use the non-quantum solutions like `train_svm` you may want to use more training examples. the parameter `--n` controls this.

## Introduction

#### Outline

- What is a quantum circuit
- How do they get simulated, and how are they run in reality
- What is our problem
- How might you do this classification
