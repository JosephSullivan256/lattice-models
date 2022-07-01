# lattice-models

Brute force calculator for the partition function of a lattice model with given boundary conditions.

![complete homogeneous symmetric functions!](logo.png)

## Usage

```bash
usage: main.py [-h] -r ROWS -c COLS -b BOUNDARY [-d {text,image}] [--calc-part-fn]

Compute Possible Lattice Model States

optional arguments:
  -h, --help            show this help message and exit
  -r ROWS, --rows ROWS  rows
  -c COLS, --cols COLS  columns
  -b BOUNDARY, --boundary BOUNDARY
                        set boundary condition
  -d {text,image}, --display-mode {text,image}
  --calc-part-fn
```

## Example

```bash
python main.py -r 3 -c 3 -b="-+++++-+++++" --calc-part-fn

 ⊖ ⊕ ⊕
⊕+?+?+⊕
 ? ? ?
⊕+?+?+⊕
 ? ? ?
⊕+?+?+⊕
 ⊕ ⊕ ⊖

z1**2 + z1*z2 + z1*z3 + z2**2 + z2*z3 + z3**2
```