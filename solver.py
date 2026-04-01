
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



def solve_max_coloring(G, n, k):
    """
    Find the largest subset V' of V such that the induced subgraph
    on V' is k-colorable.

    start by trying all n vertices, then
    decrease if not satisfiable
    """
    edges = list(G.edges())

    # Try to find the maximum number of active vertices using binary search
    # then linear refinement

    def try_at_least(min_active):
        """Check if we can color at least min_active vertices with k colors."""
        solver = Glucose3()

        # For each active vertex, it must have exactly one color
        for v in range(n):
            color_vars = [var_color(v, c, k) for c in range(k)]
            act = var_active(v, k, n)

            # If vertex is active, it must have at least one color
            # active(v) => OR(color(v,c) for c in 0..k-1)
            solver.add_clause([-act] + color_vars)

            # If vertex is active, it must have at most one color
            # For each pair of colors c1 < c2:
            # active(v) => NOT(color(v,c1) AND color(v,c2))
            for c1 in range(k):
                for c2 in range(c1 + 1, k):
                    solver.add_clause([-act, -var_color(v, c1, k), -var_color(v, c2, k)])

            # If vertex is NOT active, it should have no color
            for c in range(k):
                solver.add_clause([act, -var_color(v, c, k)])

        # For each edge (u,v): if both active, they must have different colors
        for u, v in edges:
            for c in range(k):
                # NOT(active(u) AND active(v) AND color(u,c) AND color(v,c))
                solver.add_clause([
                    -var_active(u, k, n),
                    -var_active(v, k, n),
                    -var_color(u, c, k),
                    -var_color(v, c, k)
                ])

        # At least min_active vertices must be active
        active_vars = [var_active(v, k, n) for v in range(n)]
        top_var = n * k + n  

        if min_active > 0:
            atl_clauses = CardEnc.atleast(
                lits=active_vars,
                bound=min_active,
                top_id=top_var,
                encoding=EncType.totalizer
            )
            for clause in atl_clauses:
                solver.add_clause(clause)

        result = solver.solve()
        model = solver.get_model() if result else None
        solver.delete()
        return result, model

    # Binary search for the maximum number of active vertices
    lo, hi = 0, n
    best_model = None
    best_count = 0

    # First check if all n vertices can be colored
    sat, model = try_at_least(n)
    if sat:
        best_model = model
        best_count = n
    else:
        # Binary search
        while lo <= hi:
            mid = (lo + hi) // 2
            sat, model = try_at_least(mid)
            if sat:
                best_model = model
                best_count = mid
                lo = mid + 1
            else:
                hi = mid - 1

    # Extract solution from model
    coloring = {}
    if best_model is not None:
        model_set = set(best_model)
        for v in range(n):
            if var_active(v, k, n) in model_set:
                for c in range(k):
                    if var_color(v, c, k) in model_set:
                        coloring[v] = c
                        break

    return coloring

    # Binary search for the maximum number of active vertices
    low, high = 0, n
    best_model = None
    best_count = 0

    # First check if all n vertices can be colored
    sat, model = try_at_least(n)
    if sat:
        best_model = model
        best_count = n
    else:
        # Binary search
        while lo <= hi:
            mid = (low + high) // 2
            sat, model = try_at_least(mid)
            if sat:
                best_model = model
                best_count = mid
                low = mid + 1
            else:
                high = mid - 1

    # Extract solution from model
    coloring = {}
    if best_model is not None:
        model_set = set(best_model)
        for v in range(n):
            if var_active(v, k, n) in model_set:
                for c in range(k):
                    if var_color(v, c, k) in model_set:
                        coloring[v] = c
                        break

    return coloring


def main():
    if len(sys.argv) != 4:
        print("Usage: ./solver N k p", file=sys.stderr)
        sys.exit(1)

    N = int(sys.argv[1])
    k = int(sys.argv[2])
    p = float(sys.argv[3])

    # Generate random graph
    G = generate_graph(N, p)

    # Get edges in sorted format (v < u)
    edges = []
    for u, v in G.edges():
        a, b = min(u, v), max(u, v)
        edges.append(f"{a}-{b}")
    # Sort edges for consistent output
    edges.sort(key=lambda e: (int(e.split('-')[0]), int(e.split('-')[1])))

    # Print edges
    print(" ".join(edges))

    # Solve
    coloring = solve_max_coloring(G, N, k)

    # Print colorings sorted by vertex
    color_strs = [f"{v}:{c}" for v, c in sorted(coloring.items())]
    print(" ".join(color_strs))


if __name__ == "__main__":
    main()

