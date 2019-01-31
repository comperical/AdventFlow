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

This may seem confusing, but it is quite easy to learn.
Also, the diagram extraction technique introduces a new step in your programming workflow.
It is a quite productive workflow 
	to edit the transition map, rebuild the flow diagram, examine it to detect mistakes, and repeat.
If you make a mistake specifying the transition codes,
	you will quickly realize it when you look at the flow diagram.
