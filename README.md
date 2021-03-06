# lattice-models

Brute force calculator for the partition function of a lattice model with given boundary conditions.

![complete homogeneous symmetric functions!](logo.png)

## Usage

```
$ python latmod_calc.py -h
usage: latmod_calc.py [-h] -r ROWS -c COLS -b BOUNDARY [-d {text,image}] [--calc-part-fn {display text,display image,quiet,none}]

Compute Possible Lattice Model States

optional arguments:
  -h, --help            show this help message and exit
  -r ROWS, --rows ROWS  rows
  -c COLS, --cols COLS  columns
  -b BOUNDARY, --boundary BOUNDARY
                        set boundary condition
  -d {text,image}, --display-mode {text,image}
  --calc-part-fn {display text,display image,quiet,none}
                        calculate partition function
```

## Example

```
$ python latmod_calc.py -r 3 -c 3 -b="-+++++-+++++" --calc-part-fn="quiet"

 ⊖ ⊕ ⊕
⊕+?+?+⊕
 ? ? ?
⊕+?+?+⊕
 ? ? ?
⊕+?+?+⊕
 ⊕ ⊕ ⊖

z1**2 + z1*z2 + z1*z3 + z2**2 + z2*z3 + z3**2
```
