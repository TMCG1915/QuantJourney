"""Plot styling and a helper that saves figures into the results/ folder."""

from pathlib import Path

import matplotlib.pyplot as plt

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

# Colours used in a fixed order across every chart (blue, orange, aqua, ...).
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#4a3aa7"]
INK = "#0b0b0b"
MUTED = "#898781"


def set_style():
    """Apply one consistent look to all figures."""
    plt.rcParams.update(
        {
            "figure.facecolor": "#fcfcfb",
            "axes.facecolor": "#fcfcfb",
            "axes.prop_cycle": plt.cycler(color=COLORS),
            "axes.edgecolor": "#c3c2b7",
            "axes.labelcolor": INK,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#e1e0d9",
            "grid.linewidth": 0.6,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": INK,
            "lines.linewidth": 1.6,
            "legend.frameon": False,
            "figure.dpi": 100,
        }
    )


set_style()


def save_figure(fig, project, filename, dpi=150):
    """Save a figure to results/<project>/<filename> and close it."""
    folder = RESULTS_DIR / project
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")
    return path
