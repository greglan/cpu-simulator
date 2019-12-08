# Instructions
The simulator has been programmed in Python and is targeting version 3.8.
The code does not need any additional packages.

# Usage
Uncomment the program you want to run in `run.py`, and then execute `python run.py` from the same directory.

# Todo
* Add a pipeline class. This could be a "empty" pipeline which amounts to no pipeline,
or a normal pipeline. This allows more flexibility in trying different pipelines and
it is easier to compare with the case of no pipeline.
* GCD benchmark
* RSA benchmark
* Ideally, all the benchmarks should be done before implementing the CPU ?
* Current stack implementation makes the code weird: must pop() from stack.next else bug
* Other memory access: check states
* Change terminology: NOP/WAIT/STALL instructions and None. When fixing None, can remove many "if instr is not None" checks
* Round the statistics
