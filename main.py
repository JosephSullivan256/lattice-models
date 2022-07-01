from sympy import symbols
import argparse

from lattice_model import Vertex, LatticeModel
from lattice_model_state import LatticeModelState

from util import wtv, get_image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute Possible Lattice Model States')
    parser.add_argument('-r', '--rows', type=int, required=True, help="rows")
    parser.add_argument('-c', '--cols', type=int, required=True, help="columns")
    parser.add_argument('-b', '--boundary', type=str, required=True, help="set boundary condition")
    parser.add_argument('-d', '--display-mode', choices=['text', 'image'], default='text')
    parser.add_argument('--calc-part-fn', action='store_true')

    args = parser.parse_args()

    admissable_verts = [
        Vertex("++++", lambda r, c: 1),
        Vertex("----", lambda r, c: 0),
        Vertex("-+-+", lambda r, c: 1),
        Vertex("+-+-", lambda r, c: symbols('z' + str(r + 1))),
        Vertex("++--", lambda r, c: symbols('z' + str(r + 1))),
        Vertex("--++", lambda r, c: 1)
    ]

    latmod = LatticeModel(args.rows, args.cols, admissable_verts)
    state = LatticeModelState(latmod)
    state.set_boundary(wtv(args.boundary))

    if args.display_mode == 'text':
        state.print()
    elif args.display_mode == 'image':
        get_image(state)

    if args.calc_part_fn:
        print(state.compute_partition_function())
