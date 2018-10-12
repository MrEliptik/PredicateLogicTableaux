class Atom:
    #This class represents propositional logic variables in modal logic formulas.
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Atom) and other.name == self.name

    def __str__(self):
        return str(self.name)

class Implies:
    # Describes implication derived from classic propositional logic
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " -> " + self.right.__str__() + ")"

class Equivalence:
    # Describes equivalence derived from classic propositional logic
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " <-> " + self.right.__str__() + ")"

class Not:
    # Describes negation derived from classic propositional logic
    def __init__(self, inner):
        self.inner = inner

    def __eq__(self, other):
        return self.inner == other.inner

    def __str__(self):
        return u"\uFFE2" + str(self.inner)

class And:
    # Describes and derived from classic propositional logic
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2227" + " " + self.right.__str__() + ")"

class Or:
    # Describes or derived from classic propositional logic
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "(" + self.left.__str__() + " " + u"\u2228" + " " + self.right.__str__() + ")"

# Create the tree until it's exhausted 
# An opened and finished branch is a solution
class ProofTree:
    def __init__(self, formula):
        self.root_node = self.create_node(formula, [])
        self.is_closed = None
        self.solutions = []

    def create_node(self, formulas, children):
        return Node(formulas, children)

    def derive(self):
        next_node = self.root_node.__next__()

        while next_node is not None:
            node = self.expand_node(next_node)
            if(node == -1):
                # Branch is finished, check if open by verifying that there's no conflict
                if(check_conflict(next_node)):
                    # There's a conflict, branch is closed
                    next_node.is_closed = True
                    #print('Closed branch : [%s]' % ', '.join(map(str, next_node.formulas)))
                else:
                    # Branch is open
                    next_node.is_opened = True
                    self.solutions.append(next_node.formulas)
                next_node.add_child(None)   
            else:
                next_node.add_child(node)
            next_node.is_derived = True           
            next_node = self.root_node.__next__()

    # Contains all rules of tableau calculus and tries to match them to a node
    def expand_node(self, node):   
        # Determines the formula to compute based on the rules
        index = whatToCompute(node.formulas)
        if(index == -1):
            # Branch is finished, is it open ?
            return -1

        if isinstance(node.formulas[index], Atom):
            return None

        if isinstance(node.formulas[index], Not):
            formula = node.formulas[index].inner
            if isinstance(formula, Not):
                # Modifiy the formula to compute
                formulas = node.formulas.copy()
                formulas[index] = formula.inner
                return self.create_node(formulas, [])

            if isinstance(formula, And):
                # List of formulae
                formulas_left = node.formulas.copy()
                formulas_right = node.formulas.copy()

                # Create two different lists with the modified formula
                formulas_left[index] = Not(formula.left)
                formulas_right[index] = Not(formula.right)

                # Create a node for each new list of formulae
                first_node = self.create_node(formulas_left, [])
                second_node = self.create_node(formulas_right, [])
                return [first_node, second_node]

            if isinstance(formula, Or):
                # List of formulae
                formulas = node.formulas.copy()

                # Add a new formula to the list
                formulas.append(Not(formula.left))

                # Modify the indexed formula
                formulas[index] = Not(formula.right)
                return self.create_node(formulas, [])

            if isinstance(formula, Implies):
                # List of formulae
                formulas = node.formulas.copy()

                # Add a new formula to the list
                formulas.append(Not(formula.right))

                # Modify the indexed formula
                formulas[index] = formula.left
                return self.create_node(formulas, [])
            
            if isinstance(formula, Equivalence):
                # List of formulae
                formulas_left = node.formulas.copy()
                formulas_right = node.formulas.copy()

                # Create two different lists with the modified formula
                formulas_left[index] = And(formula.left, Not(formula.right))
                formulas_right[index] = And(Not(formula.left), formula.right)

                # Create a node for each new list of formulae
                first_node = self.create_node(formulas_left, [])
                second_node = self.create_node(formulas_right, [])
                return [first_node, second_node]

            if isinstance(formula, Atom):
                return None

            return None

        if isinstance(node.formulas[index], And):
            # List of formulae
            formulas = node.formulas.copy()

            # Add a new formula to the list
            formulas.append(node.formulas[index].right)

            # Modify the indexed formula
            formulas[index] = node.formulas[index].left
            return self.create_node(formulas, [])

        if isinstance(node.formulas[index], Or):
            # List of formulae
            formulas_left = node.formulas.copy()
            formulas_right = node.formulas.copy()

            # Create two different lists with the modified formula
            formulas_left[index] = node.formulas[index].left
            formulas_right[index] = node.formulas[index].right

            # Create a node for each new list of formulae
            first_node = self.create_node(formulas_left, [])
            second_node = self.create_node(formulas_right, [])
            return [first_node, second_node]

        if isinstance(node.formulas[index], Implies):
            # List of formulae
            formulas_left = node.formulas.copy()
            formulas_right = node.formulas.copy()

            # Create two different lists with the modified formula
            formulas_left[index] = Not(node.formulas[index].left)
            formulas_right[index] = node.formulas[index].right

            # Create a node for each new list of formulae
            first_node = self.create_node(formulas_left, [])
            second_node = self.create_node(formulas_right, [])            
            return [first_node, second_node]
        
        if isinstance(node.formulas[index], Equivalence):
            # List of formulae
            formulas_left = node.formulas.copy()
            formulas_right = node.formulas.copy()

            # Create two different lists with the modified formula
            formulas_left[index] = And(node.formulas[index].left, node.formulas[index].right)
            formulas_right[index] = And(Not(node.formulas[index].left), Not(node.formulas[index].right))

            # Create a node for each new list of formulae
            first_node = self.create_node(formulas_left, [])
            second_node = self.create_node(formulas_right, [])        
            return [first_node, second_node]

        return None

    def __str__(self):
        if(not self.solutions):
            return 'Tree is exhausted, no solution'
        else:
            for s in self.solutions:
                string = ('[%s]' % ', '.join(map(str, s)))
                string += ', '
            return string

# Returns the index of the formula to be computed
# based on the rule of what to compute first (trunk, not)
def whatToCompute(formulas):
    potential_index = -1
    for index, f in enumerate(formulas):
        # Determines if the formula is going to get us a trunk
        if(isinstance(f, And) or (isinstance(f, Not) and (isinstance(f.inner, Or) or isinstance(f.inner, Implies) or isinstance(f.inner, Not))) ):
            return index
        # Potential if not an Atom and not a Not(Atom)
        elif(not isinstance(f, Atom) and not( (isinstance(f, Not) and isinstance(f.inner, Atom)) )):
            # It's not the best formula to be computed first, but is a potentially computable formula
            # If nothing else is found, we compute this one
            potential_index = index
    # Return -1 if no index was found. Meaning the branch is finished (only Atoms) and maybe open ?
    return potential_index

def check_conflict(node):
    # Routine walks through each node and checks if two formula conflicts
    # ex : a, not(a)
    for index, f in enumerate(node.formulas):
        if(isinstance(f, Atom) or (isinstance(f, Not) and isinstance(f.inner, Atom))):
            for index_other, f_other in enumerate(node.formulas):
                if(index == index_other):
                    # We don't want to check a formula against itself
                    pass
                else:
                    if(isinstance(f, Atom) and isinstance(f_other, Not)):
                        if(f == f_other.inner):
                            # Conflict, close the branch !
                            return True
                    if(isinstance(f, Not) and isinstance(f_other, Atom)):
                        if(f.inner == f_other):
                            # Conflict, close the branch !
                            return True
    return False   

class Node:
    def __init__(self, formulas, children):
        self.children = children
        self.formulas = formulas
        self.is_derived = False
        self.is_opened = False
        self.is_closed = False
        self.parent = None
        self.level = 0

    def add_child(self, nodes):
        try:  
            # List of nodes
            for n in nodes:
                self.children.append(n)
        except:
            # Only one node, not a list
            self.children.append(nodes)

    def __next__(self):
         # Return next node, that is not derived yet in post order sequence.
        if self.is_derived is False:
            return self
        #if isinstance(self.children, Bottom) or isinstance(self, Bottom):
        #   return None
        else:
            for child in self.children:
                if not child.is_derived:
                    return child
                # List isn't empty, so child has no children
                if (child.children != [None] or not child.children):
                    return child.__next__()
        return None

def main():
    # p->q, q->r, p->r
    formulas = [ Implies(Atom('p'), Atom('q')), \
                Implies(Atom('q'), Atom('r')),  \
                Implies(Atom('p'), Atom('r'))   \
                ]

    # We initialize the tree with the formula
    pt = ProofTree(formulas)

    # Derive all node of the tree until the tree is exhausted or a node is open and finished
    pt.derive()

    # Print the solutions
    print('Solution for ex 1 : ' + pt.__str__())

    ############################
    # a->b, b->c, c->d, a^~d   #
    ############################
    formulas = [ Implies(Atom('a'), Atom('b')), \
                Implies(Atom('b'), Atom('c')),  \
                Implies(Atom('c'), Atom('d')),  \
                And(Atom('a'), Not(Atom('d')))  \
                ]
    pt = ProofTree(formulas)
    pt.derive()
    print('Solution for P1 : ' + pt.__str__())

    ###########################
    # a->b, b->~c, d<->c, a^d #
    ###########################
    formulas = [ Implies(Atom('a'), Atom('b')),         \
                Implies(Atom('c'), Atom('d')),          \
                Implies(Atom('e'), Atom('f')),          \
                Implies(Atom('d'), Atom('g')),          \
                Or(Atom('a'), Or(Atom('c'), Atom('e'))),\
                Atom('g'),                              \
                ]
    pt = ProofTree(formulas)
    pt.derive()
    print('Solution for P2 : ' + pt.__str__())

    ###########################
    # a->b, b->~c, d<->c, a^d #
    ###########################
    formulas = [ Implies(Atom('a'), Atom('b')),     \
                Implies(Atom('b'), Not(Atom('c'))), \
                Equivalence(Atom('c'), Atom('d')),  \
                And(Atom('a'), Atom('d'))           \
                ]
    pt = ProofTree(formulas)
    pt.derive()
    print('Solution for P3 : ' + pt.__str__())

    #####################################################################
    # avb, c<->d, e<->(a^c), e<->(b^f), b<->~c, a<->d, f<->~g, ~d, g, e #
    #####################################################################
    formulas = [ Or(Atom('a'), Atom('b')),                          \
                Equivalence(Atom('c'), Atom('d')),                  \
                Equivalence(Atom('e'), And(Atom('a'), Atom('c'))),  \
                Equivalence(Atom('e'), And(Atom('b'), Atom('f'))),  \
                Equivalence(Atom('b'), Not(Atom('c'))),             \
                Equivalence(Atom('a'), Atom('d')),                  \
                Equivalence(Atom('f'), Not(Atom('g'))),             \
                Not(Atom('d')),                                     \
                Atom('g'),                                          \
                Atom('e')                                           \
                ]
    pt = ProofTree(formulas)
    pt.derive()
    print('Solution for P4 : ' + pt.__str__())

if __name__ == '__main__':
    main()

        