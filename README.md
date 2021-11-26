# LL(1) Table Generator

For this partial, the goal was to deliver an LL(1) table generator, by applying the rules and comparing the grammar. I sticked with the python approach to handle sets and arrays in an easier way.

## Python
To execute the program, we can run it with the command 
> `python3 llGenerator.py`

## Usage
The program lets you decide between reading a file or entering data directly from console. 

It starts with a message
> LL(1) table Generator

> This generator parses a grammar to validate different inputs

> There are two ways of using the generator, from file and from command line
> Select the option: (1. From file, 2. From command line.)

and then we can chose an option. If we select option 1, it will ask for a file name
> filename: 

and if we select option 2 it will ask for the amount of productions and then it will let us enter them
> How many productions and tests are?(write them after)