import pandas as pd
import numpy as np


class HistPlot:
    def __init__(self, bins=10):
        # self.config = config
        self.bins = bins
        self.data_stack = dict()
        self.data = dict()
        self.hist_name_list = list()

        self.xlabel = "x-label"
        self.ylabel = "Count"

    def data_info(self):
        print("Current data stack:")
        self.DF = pd.DataFrame(self.data_stack)
        print(self.DF.head())

    def add_histdata(self, vals, name):
        # save to data without x ticks
        self.data[name] = vals
        # get count 'cnt' of x axis value 'xs'
        cnt, xs = np.histogram(vals, self.bins)
        xs = (xs[:-1] + xs[1:]) / 2
        self.hist_name_list.append(name)
        self.data_stack[f"{name}xs"] = xs
        self.data_stack[f"{name}cnt"] = cnt
        self.data_info()

    def add_axis_labels(self, xlabel, ylabel):
        self.xlabel = xlabel
        self.ylabel = ylabel

    def export(self, path="", f_name="hist_results.csv"):
        self.f_name = f_name
        print("**Export**\n")
        self.data_info()
        pd.DataFrame(self.data_stack).to_csv(path + f_name, index=False)
        print("\n***********")
        print("LaTeX code:")
        print("***********\n")
        self.LaTeXcode()

    def LaTeXcode(self, imports=False, caption="Caption of the histogram."):
        if imports:
            print("\tDon´t forget to import the packages:\n")
            print(r"\usepackage{graphicx}")
            print(r"\usepackage{tikz,pgfplots}")
            print("\n*\t*********\n")
        print(r"\begin{figure}[h]")
        print(r"    \centering")
        print(r"    \tikzstyle{every node}=[font=\footnotesize]")
        print(r"    \begin{tikzpicture}")
        print(r"        \begin{axis}[")
        print(f"            ylabel={self.ylabel},")
        print(f"            xlabel={self.xlabel},")
        print(r"            % xtick={0,1,...,10},")
        print(r"            width=7.5cm,")
        print(r"            height=3cm,")
        print(r"            at={(0cm,0cm)},")
        print(r"            scale only axis,")
        print(r"            axis background/.style={fill=white},")
        print(r"            grid=both,")
        print(r"            legend columns = " + str(len(self.hist_name_list)) + ",")
        print(
            r"            legend style={at={(0,1.05)}, legend cell align=left, align=left, draw=white!15!black, mark options={draw=none}, anchor=south west},"
        )
        print(r"         ]")
        # plot all y_list components
        for yn in self.hist_name_list:
            print(r"        \addplot[ybar,fill, fill opacity=0.3, black] ")
            print(
                f"        	table[x={yn}xs,y={yn}cnt,col sep=comma]"
                + r"{"
                + f"{self.f_name}"
                + "};"
            )
            print(r"        \addlegendentry{" + yn + r"};")
        print(r"        \end{axis}")
        print(r"    \end{tikzpicture}")
        print(r"    \caption{" + caption + "}")
        print(r"    \label{fig:" + caption + "}")
        print(r"\end{figure}")
