from argparse import ArgumentParser, Namespace
from os import listdir
from os.path import isdir
from pathlib import Path
from typing import Hashable, List

import pandas
from matplotlib import pyplot as plt
from pandas import DataFrame, Series
from pandas.core.groupby.generic import DataFrameGroupBy
from pandas.errors import ParserError
from progress.bar import Bar


def plot(df: DataFrame, outputFilePath: Path) -> None:
    df.plot(
        kind="bar",
        x="library",
        y="projectCount",
        logy=True,
        legend=None,
        figsize=(10, 5),
        ylim=(1, 25000),
    )

    plt.ylabel(ylabel="# of Projects")
    plt.xlabel(xlabel="Library Name")
    plt.xticks(rotation=45, ha="right", fontsize="large")

    ax = plt.gca()
    bars = ax.bar(
        df["library"],
        df["projectCount"],
        align="center",
    )

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 1),
            fontsize="medium",
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    print(plt.rcParams["figure.figsize"])
    plt.tight_layout()
    plt.savefig(outputFilePath)


def main() -> None:
    df: DataFrame = pandas.read_csv(filepath_or_buffer="newData.csv")
    print(df.columns)
    df.sort_values(by="projectCount", axis=0, ascending=False, inplace=True)
    plot(df=df, outputFilePath=Path("test2.pdf"))


if __name__ == "__main__":
    main()
