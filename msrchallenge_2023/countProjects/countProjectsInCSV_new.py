from pathlib import Path

import pandas
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from pandas import DataFrame


def plot(df: DataFrame, outputFilePath: Path) -> None:
    labelFontSize: int = 18

    df.plot(
        kind="bar",
        x="library",
        y="projectCount",
        logy=True,
        legend=None,
        figsize=(10, 5),
    )

    plt.ylabel(ylabel="# of Projects", fontsize=labelFontSize)
    plt.xlabel(xlabel="Library Name", fontsize=labelFontSize)
    plt.xticks(rotation=45, ha="right", fontsize="large")

    ax: Axes = plt.gca()
    bars = ax.bar(
        df["library"],
        df["projectCount"],
        align="center",
    )

    ax.yaxis.set_major_formatter

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 1),
            fontsize=10,
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    plt.margins(y=0.08, tight=True)
    plt.tight_layout()
    plt.xlim(left=-0.8)
    plt.savefig(outputFilePath)


def main() -> None:
    df: DataFrame = pandas.read_csv(filepath_or_buffer="newData.csv")
    df.sort_values(by="projectCount", axis=0, ascending=False, inplace=True)
    plot(df=df, outputFilePath=Path("test2.pdf"))


if __name__ == "__main__":
    main()
