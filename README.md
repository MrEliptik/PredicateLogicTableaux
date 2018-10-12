# PredicateLogicTableaux
A simple tool to represent predicate logic and assess formulas using tableaux method

# Available operator 

The basic predicate logic operators (->, <->, v, ^, ~) are available through the following classes : 

    Implies(), Equivalence(), Or(), And(), Not()
 
An atom (for example p) can be represented using the following class :

    Atom('p')
  
# How to use ? 

Let's say you want to find a solution for this set of formulas : p->q, q->r, p->r.
First, create the list of formulas :
    
    formulas = [ Implies(Atom('p'), Atom('q')), \
                Implies(Atom('q'), Atom('r')),  \
                Implies(Atom('p'), Atom('r'))   \
                ]

Then create a tree :

    # We initialize the tree with the formula
    pt = ProofTree(formulas)

And finally derive it and print the solution(s) :

    # Derive all node of the tree until the tree is exhausted or a node is open and finished
    pt.derive()

    # Print the solutions
    print('Solution for ex 1 : ' + pt.__str__())
    
The solution are printed or a message indicate that the tree is exhausted if no solutions were found :

    Solution for ex 1 : [￢p, ￢q, ￢p]
    
or 

    Tree is exhausted, no solution
    
# TODO

- Find all solutions (the program only returns maximum 1 solution)
