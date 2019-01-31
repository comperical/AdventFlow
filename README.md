## Advent Flow

These are solutions to the 2018 Advent of Code, created by Eric Wastl. 
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
	
	
### Using the Technique

To use the control flow technique, first create an object that subclasses `FiniteStateMachine` 
	in the `finite_state` package.
The abstract FSM class contains all of the logic about how to move the machine from state to state,
	while your code provides the specifics about what each state means, 
	and how the states are connected.
	
Each state in the FSM corresponds to a method on your new object.
However, not all methods will become states; this would actually be very inconvenient.
To mark a method as an FSM state, you must name it according to a naming convention.
The naming convention is `sIDX__STATENAME`, where IDX is an integer from 0 to 100, and STATENAME
	is the name of the state.
Note the double space between the IDX and the STATENAME.
It is strongly recommended to use camel case style for the state names. 
So a couple of good method names are:

1. `s8_have_more_requests`
1. `s9_already_have_request`
1. `s16_is_zero_xboundary`
1. `s23_have_above_neighbor_info`





