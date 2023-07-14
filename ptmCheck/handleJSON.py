from argparse import ArgumentParser, Namespace
from os import listdir
from pathlib import Path
from pprint import pprint as print
from typing import List

import numpy
import pandas
from matplotlib import pyplot as plt
from pandas import DataFrame, Series
from progress.bar import Bar


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Path to folder containing JSON files",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="A JSON file to dump data",
    )
    return parser.parse_args()


def toNone(x) -> None:
    return None


def main() -> None:
    args: Namespace = getArgs()

    dfList: List[DataFrame] = []
    jsonFiles: List[str] = listdir(path=args.input)

    with Bar("Reading JSON files to DataFrames... ", max=len(jsonFiles)) as bar:
        f: str
        for f in jsonFiles:
            filepath: Path = Path(args.input, f)
            df: DataFrame = pandas.read_json(
                path_or_buf=filepath, orient="index"
            ).reset_index()
            df.columns = ["repo", "calls"]
            dfList.append(df)
            bar.next()

    df: DataFrame = pandas.concat(objs=dfList, ignore_index=True)

    newDF: DataFrame = (
        df.groupby(by=["repo"]).aggregate(func={"calls": "sum"}).reset_index()
    )
    newDF.sort_values(by="calls", ignore_index=True, inplace=True)

    top15: DataFrame = newDF.tail(n=15)

    top15.plot(kind="bar", x="repo", y="calls", logy=True, legend=None)
    plt.ylabel(ylabel="# of Projects Using Model")
    plt.xlabel(xlabel="Model Name")
    plt.xticks(rotation=45, ha="right")
    plt.title(label="Top 15 Models Used in Projects")

    ax = plt.gca()
    bars = ax.bar(top15["repo"], top15["calls"])

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 1),
            fontsize="xx-small",
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig("test.pdf")


if __name__ == "__main__":
    main()
