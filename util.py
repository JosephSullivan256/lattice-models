import sys
from subprocess import call

from PIL import Image

value_dict = {
    "+": 1,
    "-": -1,
    " ": 0
}


# word to values
def wtv(word):
    return [value_dict[c] for c in list(word)]


def get_image(state, show=True, name="out.png"):
    f = open('tikz.tex', 'w')
    f.write(
        """\\documentclass{standalone}
        \\usepackage{tikz}
        \\newcommand{\\vertex}[6]{
            \\begin{scope}[xshift=#1 cm, yshift=#2 cm]
            \\coordinate (0) at (0, 0.5);
            \\coordinate (1) at (0.5, 0);
            \\coordinate (2) at (0, -0.5);
            \\coordinate (3) at (-0.5, 0);
            \\draw (0)--(0,0);
            \\draw (1)--(0,0);
            \\draw (2)--(0,0);
            \\draw (3)--(0,0);
            \\draw[fill=white] (0) circle (.15);
            \\draw[fill=white] (1) circle (.15);
            \\draw[fill=white] (2) circle (.15);
            \\draw[fill=white] (3) circle (.15);
            \\node at (0) {#3};
            \\node at (1) {#4};
            \\node at (2) {#5};
            \\node at (3) {#6};
        \\end{scope} }
        \\begin{document}
        """)
    state.write_tikz(f)
    f.write("\n\\end{document}\n")
    f.close()
    p = call(["pdflatex", 'tikz.tex'], stdout=sys.stderr)
    call(["inkscape", '--export-width=512', '--export-filename=' + name, 'tikz.pdf'])

    if show:
        img = Image.open(name)
        img.show()
