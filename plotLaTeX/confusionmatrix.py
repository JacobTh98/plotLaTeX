import numpy as np


class ConfusionMatrix:
    """
    Convert a confusion matrix into TikZ/pgfplots 'matrix plot' code
    WITHOUT exporting a CSV (values are embedded inline).
    """

    def __init__(self, cm=None, labels=None):
        self.cm = None
        self.labels = None
        self.n_classes = None

        if cm is not None and labels is not None:
            self.from_confusion_matrix(cm, labels)

    def from_confusion_matrix(self, cm: np.ndarray, labels):
        cm = np.asarray(cm)
        if cm.ndim != 2 or cm.shape[0] != cm.shape[1]:
            raise ValueError(f"cm must be a square 2D array. Got shape {cm.shape}.")
        if len(labels) != cm.shape[0]:
            raise ValueError(
                f"labels length must match cm size. Got {len(labels)} vs {cm.shape[0]}."
            )

        self.cm = cm.astype(float)
        self.labels = list(labels)
        self.n_classes = cm.shape[0]
        return self

    def from_y(self, y_true, y_pred, labels=None):
        from sklearn.metrics import confusion_matrix

        cm = confusion_matrix(y_true, y_pred, labels=labels)
        if labels is None:
            uniq = np.unique(np.concatenate([np.asarray(y_true), np.asarray(y_pred)]))
            labels = list(uniq)
        return self.from_confusion_matrix(cm, labels)

    @staticmethod
    def _escape_tex(s: str) -> str:
        repl = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }
        out = str(s)
        for k, v in repl.items():
            out = out.replace(k, v)
        return out

    def _long_rows(self, normalize=True, decimals=2):
        """
        Returns rows: (x, y, C) where:
          x = predicted class index
          y = true class index
          C = value (percent or count)
        """
        if self.cm is None:
            raise RuntimeError(
                "No confusion matrix loaded. Call from_confusion_matrix(...) or from_y(...)."
            )

        cm = self.cm.copy()
        if normalize:
            total = cm.sum()
            cm = (cm / total) * 100.0 if total > 0 else np.zeros_like(cm)

        cm = np.round(cm, decimals)

        rows = []
        for y in range(self.n_classes):
            for x in range(self.n_classes):
                rows.append((x, y, float(cm[y, x])))
        return rows

    def tikz(
        self,
        xlabel="Predicted material",
        ylabel="True material",
        width="5cm",
        height="5cm",
        colormap_name="blue",
        normalize=True,
        decimals=2,
        draw_color="gray",
        point_meta_min=0.0,
        point_meta_max=100.0,
        show_percent_node=True,
        percent_node_pos=(5.1, 1.55),
    ) -> str:
        """
        Generate TikZ/pgfplots code (inline table), matching your style.
        """
        if self.labels is None or self.n_classes is None:
            raise RuntimeError("No labels/classes loaded.")

        xticklabels = ", ".join(self._escape_tex(l) for l in self.labels)
        yticklabels = ", ".join(self._escape_tex(l) for l in self.labels)

        n = self.n_classes
        tick_range = f"0,...,{n-1}"

        rows = self._long_rows(normalize=normalize, decimals=decimals)

        # Inline table body
        table_lines = ["x y C"]
        for x, y, c in rows:
            table_lines.append(f"{x} {y} {c}")

        table_block = "\n\t\t\t" + "\n\t\t\t".join(table_lines)

        lines = []
        lines.append("% imports")
        lines.append("\\usepackage{tikz}")
        lines.append("\\usepackage{pgfplots}")
        lines.append("\\pgfplotsset{compat=1.18}")
        lines.append(
            "\\usetikzlibrary{shapes,positioning,fit,arrows.meta,decorations.pathreplacing}"
        )
        lines.append("")
        lines.append("\\begin{tikzpicture}[]")
        lines.append("	\\begin{axis}[")
        lines.append(f"		width={width},")
        lines.append(f"		height={height},")
        lines.append(f"		colormap={{{colormap_name}}}{{color=(white) color=(blue)}},")
        lines.append(f"		xticklabels={{{xticklabels}}},")
        lines.append(f"		xtick={{{tick_range}}},")
        lines.append("		xtick style={draw=none},")
        lines.append(f"		yticklabels={{{yticklabels}}},")
        lines.append(f"		ytick={{{tick_range}}},")
        lines.append("		ytick style={draw=none},")
        lines.append(f"		xlabel={{{self._escape_tex(xlabel)}}},")
        lines.append(f"		ylabel={{{self._escape_tex(ylabel)}}},")
        lines.append("		enlargelimits=false,")
        lines.append("		colorbar,")
        lines.append("		colorbar style={")
        lines.append(
            "			plot graphics/node/.style={scale=1.33,anchor=south west,inner sep=0pt,},"
        )
        lines.append("			ytick={0,20,40,60,80,100},")
        lines.append("			yticklabels={0,0.2,0.4,0.6,0.8,1.0},")
        lines.append("			yticklabel={\\pgfmathprintnumber\\tick},")
        lines.append("			yticklabel style={")
        lines.append("				/pgf/number format/fixed,")
        lines.append("				/pgf/number format/precision=1}")
        lines.append("		},")
        lines.append(
            f"		point meta min={point_meta_min},point meta max={point_meta_max},"
        )
        lines.append("		nodes near coords={\\pgfmathprintnumber\\pgfplotspointmeta},")
        lines.append("		nodes near coords style={")
        lines.append("			yshift=-7pt,")
        lines.append("			/pgf/number format/fixed,")
        lines.append(f"			/pgf/number format/precision={int(decimals)}}},")
        lines.append("		]")
        lines.append("		\\addplot[")
        lines.append("			matrix plot,")
        lines.append(f"			mesh/cols={n},")
        lines.append(f"			point meta=explicit,draw={draw_color}")
        lines.append("		] table [meta=C] {")
        lines.append(table_block)
        lines.append("		};")
        lines.append("	\\end{axis}")

        if show_percent_node:
            x0, y0 = percent_node_pos
            lines.append("")
            lines.append(
                f"	\\node [align=right, anchor = south] at ({x0},{y0}) {{\\footnotesize{{\\%}}}};"
            )

        lines.append("\\end{tikzpicture}")

        return "\n".join(lines)
