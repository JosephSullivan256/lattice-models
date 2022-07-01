from functools import reduce

from sympy import symbols
import argparse

from lattice.lattice_model import Vertex, LatticeModel
from lattice.lattice_model_state import LatticeModelState

from util import wtv, get_image, setup_directories

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute Possible Lattice Model States')
    parser.add_argument('-r', '--rows', type=int, required=True, help="rows")
    parser.add_argument('-c', '--cols', type=int, required=True, help="columns")
    parser.add_argument('-b', '--boundary', type=str, required=True, help="set boundary condition")
    parser.add_argument('-d', '--display-mode', choices=['text', 'image'], default='text')
    parser.add_argument('--calc-part-fn', choices=['display text', 'display image', 'quiet', 'none'], default='none',
                        help='calculate partition function')

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

    setup_directories()
    if args.display_mode == 'text':
        print()
        state.print()
    elif args.display_mode == 'image':
        get_image(state)

    reducer = None

    if args.calc_part_fn == 'display text':
        def temp(sum, tup):
            i, s = tup
            s.print()
            return sum+s.compute_weight()
        reducer = temp
    elif args.calc_part_fn == 'display image':
        def temp(sum, tup):
            i, s = tup
            get_image(s, False, "out" + str(i) + ".png")
            return sum+s.compute_weight()
        reducer = temp
    elif args.calc_part_fn == 'quiet':
        def temp(sum, tup):
            i, s = tup
            return sum+s.compute_weight()
        reducer = temp

    if args.calc_part_fn != 'none':
        print(reduce(
            reducer,
            enumerate(state.iter_solutions()),
            0
        ))


