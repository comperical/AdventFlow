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


