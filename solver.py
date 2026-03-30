
import sys
import networkx as nx
from pysat.solvers import Glucose3
from pysat.card import CardEnc, EncType
 
 
def generate_graph(n, p):
    """Generate a random Erdos-Renyi graph G(n, p)."""
    G = nx.gnp_random_graph(n, p)
    return G

def var_color(v, c, k):
    """Variable id for 'vertex v has color c'. 1-indexed for SAT."""
    return v * k + c + 1


def var_active(v, k, n):
    """Variable id for 'vertex v is in the subset V''. """
    return n * k + v + 1