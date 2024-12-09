import numpy as np


def calculate_props(data):
    data = np.sort(np.asarray(data))
    median = np.median(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_whisker = data[data >= (q1 - 1.5 * iqr)].min()
    upper_whisker = data[data <= (q3 + 1.5 * iqr)].max()
    return {
        "median": median,
        "lower_quartile": q1,
        "upper_quartile": q3,
        "lower_whisker": lower_whisker,
        "upper_whisker": upper_whisker,
    }


class BoxPlot:
    def __init__(self, bins=10):
        # self.config = config
        self.data_names = list()
        self.data = list()
        self.xlabel = "x-label"
        self.ylabel = "y-label"

    def data_info(self):
        for ele, data in zip(self.data_names, self.data):
            print(ele)
            print(data)

    def add_data(self, data, x_name):
        self.data_names.append(x_name)
        self.data.append(calculate_props(data))
        self.data_info()

    def add_axis_labels(self, xlabel, ylabel):
        self.xlabel = xlabel
        self.ylabel = ylabel

    def export(self, path="", f_name="boxplot_results.csv"):
        self.f_name = f_name
        print("**Export**\n")
        self.data_info()
        print("\n***********")
        print("LaTeX code:")
        print("***********\n")
        self.LaTeXcode()

    def LaTeXcode(self, imports=True, caption="Caption of the boxplot."):
        if imports:
            print("\tDon´t forget to import the packages:\n")
            print(r"\usepackage{graphicx}")
            print(r"\usepackage{tikz,pgfplots}")
            print(r"\usepgfplotslibrary{statistics}")
            print("\n*\t*********\n")
        print(r"\begin{figure}[h]")
        print(r"    \centering")
        print(r"    \tikzstyle{every node}=[font=\footnotesize]")
        print(r"    \begin{tikzpicture}")
        print(r"        \begin{axis}[")
        print(f"            ylabel={self.ylabel},")
        print(f"            xlabel={self.xlabel},")
        xtks = np.arange(1, len(self.data_names) + 1)
        print(f"            xtick={{ {', '.join(map(str, xtks))} }},")
        print(f"            xticklabels={{ {', '.join(self.data_names)} }},")
        print(r"            width=7.5cm,")
        print(r"            height=3cm,")
        print(r"            boxplot/draw direction = y,")
        print(r"            at={(0cm,0cm)},")
        print(r"            scale only axis,")
        print(r"            axis background/.style={fill=white},")
        print(r"            grid=both,")
        print(r"]")
        # plot all data points
        for ele, data in zip(self.data_names, self.data):
            print(r"            \addplot[")
            print(r"            fill,")
            print(r"            fill opacity=0.7,")
            print(r"            boxplot prepared={")
            print(f"                median={data['median']},")
            print(f"                upper quartile={data['upper_quartile']},")
            print(f"                lower quartile={data['lower_quartile']},")
            print(f"                upper whisker={data['upper_whisker']},")
            print(f"                lower whisker={data['lower_whisker']}")
            print(r"                            },")
            print(r"        ] coordinates {};")

        print(r"        \end{axis}")
        print(r"    \end{tikzpicture}")
        print(r"    \caption{" + caption + "}")
        print(r"    \label{fig:" + caption + "}")
        print(r"\end{figure}")
