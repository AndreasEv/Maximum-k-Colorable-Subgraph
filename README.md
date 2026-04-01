# EPL341 - Assignment 2: Maximum Partial Graph k-Coloring

## Description

This program solves a variant of the graph coloring optimization problem. Given a constant `k` (number of available colors), it finds the largest subset of vertices `V'` of an undirected random graph `G=(V,E)` such that the induced subgraph of `V'` can be properly colored with `k` colors.

The solution uses **SAT-based optimization** via the PySAT library, with binary search over the number of active (colored) vertices and cardinality constraints to maximize the subset size.

## Requirements

- Python 3
- [PySAT](https://github.com/pysathq/pysat)
- [NetworkX](https://networkx.org/)

## Installation

```bash
pip install python-sat networkx
```

## Execution

```bash
python3 solver.py N k p
```

Where:
- `N` — number of vertices in the graph (|V|)
- `k` — number of available colors
- `p` — probability of an edge between each pair of vertices (Erdős–Rényi model)

### Example

```bash
python3 solver.py 5 2 0.5
```

### Output format

- **Line 1**: Edges of the generated graph, separated by spaces. Each edge is written as `v-u` where `v < u`.
- **Line 2**: Colorings of the selected vertices, separated by spaces. Each coloring is written as `v:c` where `v` is the vertex and `c` is the color (integer from 0 to k-1).

### Example output

```
0-1 0-2 0-3 1-2 2-4
0:0 1:1 3:1 4:0
```

## Making it executable (optional)

```bash
chmod +x solver.py
./solver.py 5 2 0.5
```
