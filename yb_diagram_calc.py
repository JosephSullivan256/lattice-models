from functools import reduce

from sympy import symbols, simplify
import argparse

from lattice.lattice_model import LatticeModel
from lattice.vertex import Vertex, RVertex
from lattice.lattice_model_state import LatticeModelState
from lattice.yang_baxter import YangBaxter, LeftYBState, RightYBState

from util import wtv, get_image, setup_directories

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute Possible Yang Baxter Diagram States')
    parser.add_argument('-b', '--boundary', type=str, required=True, help="set boundary condition")
    parser.add_argument('-d', '--display-mode', choices=['text', 'image'], default='text')
    parser.add_argument('--calc-part-fn', choices=['display text', 'display image', 'quiet', 'none'], default='none',
                        help='calculate partition function')

    args = parser.parse_args()
    setup_directories()

    admissable_h_verts = [
        Vertex("++++", lambda r: 1),
        Vertex("----", lambda r: 0),
        Vertex("-+-+", lambda r: 1),
        Vertex("+-+-", lambda r: symbols('z' + str(r))),
        Vertex("++--", lambda r: symbols('z' + str(r))),
        Vertex("--++", lambda r: 1)
    ]
    admissable_r_verts = [
        RVertex("++++", lambda r1, r2: symbols('z' + str(r1))),
        RVertex("----", lambda r1, r2: symbols('z' + str(r2))),
        RVertex("-+-+", lambda r1, r2: 0),
        RVertex("+-+-", lambda r1, r2: symbols('z' + str(r1))-symbols('z' + str(r2))),
        RVertex("++--", lambda r1, r2: symbols('z' + str(r1))),
        RVertex("--++", lambda r1, r2: symbols('z' + str(r2))),
    ]

    yb = YangBaxter(admissable_h_verts, admissable_r_verts)
    states = [LeftYBState(yb), RightYBState(yb)]
    boundary = args.boundary
    for i, state in enumerate(states):
        state.set_boundary(wtv(boundary))

        if args.display_mode == 'text':
            print()
            state.print()
        elif args.display_mode == 'image':
            get_image(state, True, "out" + str(i) + ".png")

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
            print(simplify(reduce(
                reducer,
                enumerate(state.iter_solutions()),
                0
            )))


