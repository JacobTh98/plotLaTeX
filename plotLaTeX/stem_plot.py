import numpy as np


class StemPlot:
    def __init__(self, layout="default", marker_size=6):
        self.layout = layout
        self.marker_size = marker_size
        self.x_label = "$k$"
        self.y_label = "$x[k]$"

    def add_xy_vals(self, x_vals, y_vals):
        assert len(x_vals) == len(y_vals)
        self.x_vals = x_vals
        self.y_vals = y_vals

    def add_xy_labels(self, x_label, y_label):
        self.x_label = x_label
        self.y_label = y_label

    def LaTeXcode(self, imports=False, caption="Stem plot caption."):
        if imports:
            print("\tDon´t forget to import the packages:\n")
            print(r"\usepackage{graphicx}")
            print(r"\usepackage{tikz,pgfplots}")
            print("\n*\t*********\n")
        print(r"\begin{figure}")
        print(r"% definition of stem style")
        print(
            r"\tikzstyle{stem}=[ycomb,mark=*,mark size="
            + str(self.marker_size)
            + r"\pgflinewidth,color=blue,thick]"
        )
        print(r"")
        print(r"    \centering")
        print(r"    \tikzstyle{every node}=[font=\footnotesize]")
        print(r"    \begin{tikzpicture}")
        print(r"        \begin{axis}[")
        print("            xlabel={" + self.x_label + "},")
        print("            ylabel={" + self.y_label + "},")

        if self.layout == "default":
            print(r"            width=7.5cm,")
            print(r"            height=3cm,")
            print(r"            at={(0cm,0cm)},")
            print(r"            scale only axis,")
            print(r"            axis background/.style={fill=white},")
            print(r"            grid=both,")

        elif self.layout == "beautiful":
            print(r"            axis lines=center,")
            print(r"            xlabel style=right,")
            print(r"            ylabel style=left,")
            print(r"            width=7.5cm,")
            print(r"            height=4cm,")
            print(f"            ymin={np.min(self.y_vals)-0.5},")
            print(f"            ymax={np.max(self.y_vals)+1.0},")
            print(f"            xmin={np.min(self.x_vals)-0.5},")
            print(f"            xmax={np.max(self.x_vals)+0.5},")
            y_ticks = np.arange(np.min(self.y_vals), np.max(self.y_vals))
            print(r"            xtick={" + ",".join(map(str, self.x_vals)) + "},")
            print(r"            ytick={" + ",".join(map(str, y_ticks)) + "},")

            print(r"            grid=both,")
            print(r"            grid style={dashed,gray!30},")
            print(r"            axis line style={thick,->},")
        print(r"            ]")
        stem_coords = " ".join(
            f"({xi},{yi})" for xi, yi in zip(self.x_vals, self.y_vals)
        )
        print(r"            \addplot[stem] plot coordinates{" + stem_coords + "};")
        print(r"        \end{axis}")
        print(r"    \end{tikzpicture}")
        print(r"    \caption{" + caption + "}")
        print(r"    \label{fig:" + caption + "}")
        print(r"\end{figure}")
