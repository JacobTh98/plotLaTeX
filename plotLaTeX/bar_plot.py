import numpy as np
from .LaTeX_colors import latex_colors


class Barplot:
    def __init__(self, dataframe, mode="default"):
        self.df = dataframe
        self.mode = mode
        self.xlabel = "x-label"
        self.ylabel = "y-label"
        self.x_labels = list(self.df.iloc[:, 0])
        self.data_info()

    def data_info(self):
        print(self.df)

    def add_axis_labels(self, xlabel, ylabel):
        self.xlabel = xlabel
        self.ylabel = ylabel

    def set_mode(self, mode):
        """
        mode=
            - default
            - multiple
            - stacked
        """
        self.bar_mode = mode

    def LaTeXcode(self, imports=True, caption="Caption of the default barchart."):
        if imports:
            print("\tDon´t forget to import the packages:\n")
            print(r"\usepackage{graphicx}")
            print(r"\usepackage{tikz,pgfplots}")
            print(r"\usepgfplotslibrary{statistics}")
            print("\n*\t*********\n")

            print(r"\begin{figure}[ht]")
            print(r"    \centering")
            print(r"    \tikzstyle{every node}=[font=\footnotesize]")
            print(r"    \begin{tikzpicture}")
            print(r"        \begin{axis}[")
            print(f"            ylabel={self.ylabel},")
            print(f"            xlabel={self.xlabel},")
            print(f"            xticklabels={{{','.join(self.x_labels)}}},")
            print(r"            ybar,")
            print(r"            bar width=0.5cm,")
            print(r"            xtick=data,")
            print(r"            width=7.5cm,")
            print(r"            height=3cm,")
            print(r"            at={(0cm,0cm)},")
            print(r"            scale only axis,")
            print(r"            axis background/.style={fill=white},")
            print(r"            grid=both,")
            print(r"            legend columns = 1,")
            print(
                r"            legend style={at={(1,1.05)}, legend cell align=left, align=left, draw=white!15!black, mark options={draw=none}, anchor=south east},"
            )
            print(r"        ]")
            print()
            print(r"        \addplot[fill=black!70!black,opacity=0.7]  ")
            coordinates = " ".join(
                f"({i+1},{row['sales']})" for i, row in self.df.iterrows()
            )
            print(f"        coordinates {{{coordinates}}};")
            # print(r"        \addlegendentry{2015};")
            print()
            print(r"        \end{axis}")
            print(r"    \end{tikzpicture}")
            print(r"    \caption{" + caption + "}")
            print(r"    \label{fig:" + caption + "}")
            print(r"\end{figure}")


class MultipleBars:
    def __init__(self, categories: list, bars: dict, mode="multiple"):
        self.categories = categories
        self.xlabel = "x-label"
        self.ylabel = "y-label"
        self.xticks = np.arange(len(categories))
        self.bars = bars
        self.mode = mode

    def add_axis_labels(self, xlabel, ylabel):
        self.xlabel = xlabel
        self.ylabel = ylabel

    def LaTeXcode(self, imports=True, caption=f"Caption of the barchart."):
        print(r"\begin{figure}[ht]")
        print(r"\centering")
        print(r"\tikzstyle{every node}=[font=\footnotesize]")
        print(r"\begin{tikzpicture}")
        print(r"    \begin{axis}[")
        print(f"            ylabel={self.ylabel},")
        print(f"            xlabel={self.xlabel},")
        print(f"            xtick={{ {', '.join(map(str, self.xticks))} }},")
        print(f"            xticklabels={{ {', '.join(self.categories)} }},")
        if self.mode == "multiple":
            print(r"            ybar,")
        elif self.mode == "stacked":
            print(r"            ybar stacked,")
        print(r"            bar width=0.3cm,")
        print(r"            xtick=data,")
        print(r"            width=7.5cm,")
        print(r"            height=3cm,")
        print(r"            at={(0cm,0cm)},")
        print(r"            scale only axis,")
        print(r"            axis background/.style={fill=white},")
        print(r"            grid=both,")
        print(f"            legend columns = {len(self.bars)},")
        print(
            r"            legend style={at={(1,1.05)}, legend cell align=left, align=left, draw=white!15!black, mark options={draw=none}, anchor=south east},"
        )
        print(r"    ]")

        for i, (x_idx, values) in enumerate(self.bars.items()):
            color = latex_colors[i]
            print(f"        \\addplot[fill={color}!70!black,opacity=0.7]")
            coordinates = " ".join(f"({i+1},{value})" for i, value in enumerate(values))
            print(f"            coordinates {{{coordinates}}};")
            print(f"        \\addlegendentry{{{x_idx}}};\n")
        print()
        print(r"    \end{axis}")
        print(r"\end{tikzpicture}")
        print(r"    \caption{" + caption + "}")
        print(r"    \label{fig:" + caption + "}")
        print(r"\end{figure}")
