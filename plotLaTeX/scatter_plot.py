import pandas as pd
import numpy as np


class ScatterPlot:
    """
    A helper class to organize and export multiple datasets for scatter plotting.
    It stores x–y matrix-like structures and can export data and produce LaTeX code.
    """

    def __init__(self):
        self.data_stack = dict()
        self.y_name_list = list()
        self.x_vals = None

    def data_info(self):
        """Print current stored data."""
        print("Current data stack:")
        self.DF = pd.DataFrame(self.data_stack)
        print(self.DF.head())

    def add_xvals(self, x_vals, x_axs_name="x"):
        """Store the common x-values used for scatter plotting."""
        print("Set x-values.")
        self.x_axs_name = x_axs_name
        self.x_vals = x_vals
        self.n_x_vals = len(x_vals)

        self.data_stack[x_axs_name] = x_vals
        self.data_info()

    def add_yvals(self, y_vals, y_name):
        """
        Add an additional dependent variable (scatter y-values).
        y_name must be unique.
        """
        self.n_y_vals = len(y_vals)

        if y_name in self.y_name_list:
            print("Please use a different name to add more y-data.")
        else:
            self.y_name_list.append(y_name)
            self.data_stack[y_name] = y_vals
            print(f"Added {y_name} with {len(y_vals)} entries.")

        self.data_info()

    def export(self, path="", f_name="scatter_results.csv"):
        """
        Export stored x–y data to a csv file.
        If no x-values were provided, create a default index.
        """
        if self.x_vals is None or len(self.x_vals) == 0:
            print("No x-values found -> using index as x-axis.")
            self.data_stack["x"] = np.arange(self.n_y_vals)

        self.f_name = f_name

        print("**Exporting scatter data**\n")
        self.data_info()

        pd.DataFrame(self.data_stack).to_csv(path + f_name, index=False)

        print("\n***********")
        print("LaTeX code for scatter plot:")
        print("***********\n")
        self.latex_code()

    def latex_code(self, imports=False, caption="Caption of the scatter plot."):
        """
        Produce pgfplots LaTeX code for scatter plots.
        """
        if imports:
            print("\tDon’t forget to import the packages:\n")
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
        print(r"            width=7.5cm,")
        print(r"            height=3cm,")
        print(r"            grid=both,")
        print(r"            legend columns=" + str(len(self.y_name_list)) + ",")
        print(
            r"            legend style={at={(0,1.05)}, anchor=south west, draw=white!15!black},"
        )
        print(r"         ]")

        # scatter plot for every y-series
        for yn in self.y_name_list:
            print(r"        \addplot+[only marks] ")
            print(
                f"            table[x={self.x_axs_name},y={yn},col sep=comma]"
                + r"{"
                + self.f_name
                + r"};"
            )
            print(r"        \addlegendentry{" + yn + r"};")

        print(r"        \end{axis}")
        print(r"    \end{tikzpicture}")
        print(r"    \caption{" + caption + "}")
        print(r"    \label{fig:" + caption.replace(" ", "_") + "}")
        print(r"\end{figure}")
