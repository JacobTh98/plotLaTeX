import pandas as pd
import numpy as np


class LinePlot:
    def __init__(self):
        # self.config = config
        self.data_stack = dict()
        self.y_name_list = list()
        self.x_vals = None

    def data_info(self):
        print("Current data stack:")
        self.DF = pd.DataFrame(self.data_stack)
        print(self.DF.head())

    def add_xvals(self, x_vals, x_axs_name="x"):
        print("Set x-ticks.")
        self.x_axs_name = x_axs_name
        self.x_vals = x_vals
        self.n_x_vals = len(x_vals)
        self.data_stack[x_axs_name] = x_vals

        self.data_info()

    def add_yvals(self, y_vals, y_name):
        self.n_y_vals = len(y_vals)
        if y_name in self.y_name_list:
            print("Please use a different name to add more data.")
        else:
            self.y_name_list.append(y_name)
            self.data_stack[y_name] = y_vals
            print(f"Added {y_name} with {len(y_vals)} entries.")
        self.data_info()

    def export(self, path="", f_name="line_results.csv"):
        if self.x_vals is None or len(self.x_vals) == 0:
            self.data_stack["x"] = np.arange(self.n_y_vals)
        self.f_name = f_name
        print("**Export**\n")
        self.data_info()
        pd.DataFrame(self.data_stack).to_csv(path + f_name, index=False)
        print("\n***********")
        print("LaTeX code:")
        print("***********\n")
        self.LaTeXcode()

    def LaTeXcode(self, imports=False, caption="Caption of the plot."):
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
        print(r"            ylabel={y-label},")
        print(r"            xlabel={x-label},")
        print(r"            % xtick={0,1,...,10},")
        print(r"            width=7.5cm,")
        print(r"            height=3cm,")
        print(r"            at={(0cm,0cm)},")
        print(r"            scale only axis,")
        print(r"            axis background/.style={fill=white},")
        print(r"            grid=both,")
        print(r"            legend columns = " + str(len(self.y_name_list)) + ",")
        print(
            r"            legend style={at={(0,1.05)}, legend cell align=left, align=left, draw=white!15!black, mark options={draw=none}, anchor=south west},"
        )
        print(r"         ]")
        # plot all y_list components
        for yn in self.y_name_list:
            print(r"        \addplot[] ")
            print(
                f"        	table[x=x,y={yn},col sep=comma]"
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
