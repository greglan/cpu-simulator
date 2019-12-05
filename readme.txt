# Instructions
The simulator has been programmed in Python and is targeting version 3.8.
The code is self-contained: no additional packages are required.

# Usage
Uncomment the progam you want to run in `run.py`, and then execute `python run.py` from the same directory.

# Todo
* Add a pipeline class. This could be a "empty" pipeline which amounts to no pipeline,
or a normal pipeline. This allows more flexibility in trying different pipelines and
it is easier to compare with the case of no pipeline.
* GCD benchmark
* RSA benchmark
* Ideally, all the benchmarks should be done before implementing the CPU ?
* When doing a branch, should clear the pipeline
* Clock count should start as soon as the program starts: fetch takes a clock cycle
* Add an additional "wait" instruction for stalling the pipeline ?
* Current stack implementation makes the code weird: must pop() from stack.next else bug
* Pad register values so that all is aligned always