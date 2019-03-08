
## Quick Glance

This is a set of problem solutions written in Python written in a special programming style
	based on the concept of Finite State Machines.
This allows us to automatically extract control flow diagrams from the source code.
Example [this diagram](diagram/p17a.png) was extracted from the PMachine
	object in [this Python file](src/p17a.py).

## Advent Flow

These are solutions to the [2018 Advent of Code](https://adventofcode.com/2018), created by Eric Wastl. 
Thanks to Eric for an enjoyable suite of problems ranging from easy to hard. 

I used these problems as a demonstration tool to showcase my "FlowState" programming technique.
This technique requires the programmer to decompose a computation in terms of a series of 
	named steps, which are methods on a special type of object.
The programmer also specifies the control flow relationships between the steps, 
	using a simple DSL.
The object is then submitted to a driver system, which performs the computation
	by querying the methods on the object and the specified control flow information.
	
Using this technique yields several advantages.
The main one is that the driver system can 
	**automatically create control flow diagrams** directly from the program specification.
You can see the extracted diagrams for the Advent problems in the `diagram` directory.
Each PNG file corresponds to a Python file in the `src` directory.
I believe these diagrams provide very useful and powerful documentation.
A reader of the code can look at the diagrams and get a very quick, clear "big picture" 
	understanding of how the computation works.
Unlike standard written documentation, the diagrams cannot be out-of-date,
	since they are extracted from the source code.

Another nice benefit of this technique is that it allows  **steppable debugging without an IDE**.
To do this, you just load the state machine object in the REPL,
	and then call various `run(...)` methods on it.
Then you can examine its behavior and data contents in different states.

The technique also gives you some nice **easy-to-interpret performance statistics**.
These statistics are obtained by logging the number of visits to each state and 
	the amount of time spent in each state.
	
<br/>
<br/>
	
	
### Using the Control Flow Technique


To use the control flow technique, first create an object that subclasses `FiniteStateMachine` 
	in the `finite_state` package.
The abstract FSM class contains all of the logic about how to move the machine from state to state,
	while your code provides the specifics about what each state means, 
	and how the states are connected.
	
Each state in the FSM corresponds to a method on your new object.
However, not all methods will become states; this would actually be very inconvenient.
To mark a method as an FSM state, you must name it according to a naming convention.
The naming convention is `sIDX_STATENAME`, where IDX is an integer from 0 to 100, and STATENAME
	is the name of the state.
It is strongly recommended to use camel case style for the state names. 
The DSL for specifying the FSM transitions is based on the *acronym* version of the state name.
Specifically, you split the state name by underscore, take the first character of each resulting token,
	and capitalize the result.
Some examples of good state-method names, and corresponding acronym codes, are:

1. `s8_have_more_requests` -- HMR
1. `s9_already_have_request` -- AHR
1. `s16_is_zero_xboundary` -- IZX
1. `s23_have_above_neighbor_info` -- HANI


The FSM transitions are specified in the object's constructor using a simple DSL based on JSON
	and the acronym versions of the state names.
The JSON object is just a key/value mapping where the key is the acronymized state name, and 
	the value indicates the outgoing transitions from the state.
Here is an example:

```python
class PMachine(FiniteStateMachine):

    def __init__(self):
        
        statemap = """
        {
            "HMR" : "F:SC",
            "AHR" : "T:PRQ",
            "RIO" : "T:ZGA",
            "RIT" : "F:IZY",
            "ZGA" : "PRQ",
            "PRQ" : "HMR",
            "IZY" : "F:IZX",
            "ZYA" : "PRQ",
            "ZXA" : "PRQ",
            "IZX" : "F:HLNI",
            "HLNI" : "F:SLR",
            "HANI" : "F:SAR",
            "SLR" : "PRQ",
            "NBA" : "PRQ"
        }
        """
        
        FiniteStateMachine.__init__(self, json.loads(statemap))
        
        # ... additional constructor information for specific machine
```

There are two types of states illustrated in the transition map.
For `op` (operation) states, there is a single outgoing transition.
For example, the state `ZGA` always leads directly to `PRQ`. 
For `query` states, there are two possibilities, depending on whether the state-method returns True or False.
For example, the state `RIT` has a transition code `F:IZY`, 
	which means that if the return value is False, the machine will transition to state `IZY`.

This might seem underspecified. 
Where does the state `RIT` transition on a True result?
Since it is not specified, the FSM driver infers the "default" transition to be 
	the state-method with the next highest index.
As we can see by looking at the code, the next state-method after `RIT` is `ZGA` (ZeroGeoAnswer).

The default transitions are also used for the operation states.
Since there is only one possible transition for an operation state,
	you often don't even need to specify it explicitly,
	if you organize the state-methods cleverly such that 
	the default transition is the correct one.
	
There is also a third state type: the `end` or completion states. 
These are shown as diamonds in the flow diagrams.
Completion states should have *no* entry in the state transition map;
	specifying a transition for a completion state is an inspection-time error.
However, you *do* need to write a state-method for the completion states.
The FSM driver detects completion states
	by finding method names that end in `_complete` or `_end`.
Important note: completion states will never run,
	so there is not much point in putting any actual code into them.

This may seem confusing, but it is quite easy to learn.
Also, the diagram extraction technique introduces a new step in your programming workflow.
It is a quite productive workflow 
	to edit the transition map, rebuild the flow diagram, examine it to detect mistakes, and repeat.
If you make a mistake specifying the transition codes,
	you will quickly realize it when you look at the flow diagram.
	
	
### FSM methods

The `FiniteStateMachine` class provides a number of utility methods that can be used to control the machine.
The meaning of these methods should be intuitively clear.


1. `run2_completion` - run the machine until it reaches an `end` state.
1. `run_one_step` - run a single step of the machine, which can be either a query or an operation.
1. `run2_step_count` - run the machine until it reaches a specific step count.
1. `run_until` - this method takes a function argument, typically a `lambda`, 
and runs the machine until the function returns true.
1. `get_state` - this will return the *full* state-method name (eg `s14_run_the_thing`) of the current state.
1. `get_state_type` - this will return the state type as a string: one of `op/query/end`. 
	
### Dependencies 

The code is written in Python 3.

The main external dependency is [GraphViz](https://www.graphviz.org/).
This is not a Python dependency; GraphViz should be installed on your system and should be findable on your path.
To create the diagrams, the FSM code generates a GV file and calls the GraphViz `dot` program as a system call.
The output is always PNG.
Of course, GraphViz is only necessary to create the diagrams.
The FSM code will run perfectly fine if GV is not installed.

There are no other dependencies in this repo.

### Experience with the Advent of Code Challenge

Overall, I had a good experience solving these problems.
However, it took much longer than I originally expected.
This is partly because I am stubborn and didn't want to ask the Internet for help.
With two exceptions mentioned below, I was able to solve all the problems on my own.

My favorite problems were P20 (A Regular Map) and P17 (Reservoir Research).
When I initially studied P20, my initial impression was that it was impossible.
I struggled with it for a while, and finally solved it on my own,
	which was enormously satisfying.
P17 was not as hard, but was still a quite elegant problem with a nice solution.
The P17 solution also created a nice control flow diagram.

I also grudgingly admit that p23 (Experimental Emergency Teleportation) was a good problem.
I was annoyed with this problem,
	because it was the one problem I was fundamentally not able to solve: 
	I had never seen the recursive partitioning technique before.
But because of this, it expanded my repertoire as a programmer. 

I had mixed feelings about the "battle" problems P15 (Beverage Bandits) 
	and P24 (Immune System Simulator 20XX).
On the one hand, they generated good control flow diagrams
	that do a good job at illustrating the idea(s) of the problems.
However, P15 in particular had a lot of really tedious points, 
	and I'm not the only one who complained about this.
I was able to solve all of the test cases, and part 1 of the problem,
	with relative ease.
However, part 2 failed due to some very obscure edge cases, 
	that I decided not to invest the time to root out: it didn't seem worthwhile.

I also had mixed feelings about the problems that used "ElfCode": 
	P16 (Chronal Classification), P19 (Go With the Flow), and P21 (Chronal Conversion).
These are problems where you are asked to simulate a device 
	that runs an special type of assembly language called ElfCode.
For P16, you basically just have to make sure that your simulation is correct;
	that's not too bad.
For P19 and P21, the computation will run for far too long by default. 
So to get the right answer, you have to study the ElfCode, determine what it does,
	and then figure out a computational shortcut.
For P19 this wasn't too bad, but for P21 it felt really tedious.
		
Other than the ones I mentioned, most of the problems didn't feel too hard.	
There were several nice problems that used standard techniques like breadth-first search (BFS)
	and Summed-Add Tables.
	
	
### Running the Code

To run all the solutions and check the answers, run:

```
python3 solve_all.py
```

This will take about 15 minutes.
To rebuild all the diagrams, run:

```
python3 all_diagrams.py
```

This will run fast.
To run a particular problem, you can use:

```
python3 entry.py PCODE solve|diagram|test|run2step [stepcount]
```

That will run the corresponding action (solve/diagram/test) for the given problem code.
If you use `run2step`, also include a stepcount.


![Mission Accomplished](https://github.com/comperical/AdventFlow/blob/master/diagram/AdventComplete.png)





