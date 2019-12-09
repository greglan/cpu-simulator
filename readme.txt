# Instructions
The simulator has been programmed in Python and is targeting version 3.8.
The code depends on matplotlib for running the experiments.

# Usage
Uncomment the program you want to run in `run.py`, and then execute `python run.py` from the same directory.

# Todo
* GCD benchmark
* RSA benchmark
* Ideally, all the benchmarks should be done before implementing the CPU ?
* Current stack implementation makes the code weird: must pop() from stack.next else bug
* Better dependency checks
* Branch prediction
* Out of order (reorder buffer)