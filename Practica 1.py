import itertools
import graphviz

def is_reflexive(relation_set):
    elements = set(itertools.chain(*relation_set))
    return all((x, x) in relation_set for x in elements)

def is_symmetric(relation_set):
    return all((y, x) in relation_set for (x, y) in relation_set)

def is_transitive(relation_set):
    return all((a, c) in relation_set for (a, b) in relation_set for (b_prime, c) in relation_set if b == b_prime)

def generate_graph(relation_set):
    dot = graphviz.Digraph(comment='Relation Graph', format='png')

    for (x, y) in relation_set:
        dot.node(str(x))
        dot.node(str(y))
        dot.edge(str(x), str(y))

    dot.render('graph', format='png', cleanup=True)

if __name__ == "__main__":
    relation_set = {(0, 0), (0, 1), (0, 3), (1, 0), (1, 1), (2, 2), (3, 0), (3, 3)}

    reflexive = is_reflexive(relation_set)
    symmetric = is_symmetric(relation_set)
    transitive = is_transitive(relation_set)

    if reflexive:
        print("(a) R is reflexive.")
    else:
        print("(a) R is not reflexive.")

    if symmetric:
        print("(b) R is symmetric.")
    else:
        print("(b) R is not symmetric.")

    if transitive:
        print("(c) R is transitive.")
    else:
        print("(c) R is not transitive.")

    if reflexive and symmetric and transitive:
        print("(d) R is an equivalence relation.")
        generate_graph(relation_set)
        print("Graph saved as 'graph.png'")
    else:
        print("(d) R is not an equivalence relation.")
