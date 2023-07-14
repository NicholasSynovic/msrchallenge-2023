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


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Path to CSV file to count repositories OR directory containing CSVs",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=False,
        default="data.csv",
        help="Path to store output CSV if analyzing a directory of files",
    )
    parser.add_argument(
        "-f",
        "--fig",
        type=Path,
        required=False,
        default="barChart.png",
        help="Path to store output figure if analyzing a directory of files",
    )
    return parser.parse_args()


def groupByRepository(df: DataFrame) -> DataFrameGroupBy:
    dfgb: DataFrameGroupBy = df.groupby(by=["repository"])
    return dfgb


def plot(df: DataFrame, outputFilePath: Path) -> None:
    df.plot(kind="bar", x="library", y="projectCount", logy=True, legend=None)

    plt.ylabel(ylabel="# of Projects")
    plt.xlabel(xlabel="Library Name")
    plt.xticks(rotation=45, ha="right", fontsize="x-small")
    plt.title(label="# of Projects per Library")

    ax = plt.gca()
    bars = ax.bar(df["library"], df["projectCount"])

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
    plt.savefig(outputFilePath)


def main() -> None:
    args: Namespace = getArgs()

    if isdir(s=args.input):
        data: dict[str, List[str | int]] = {"library": [], "projectCount": []}

        fileList: List[Path] = [Path(args.input, f) for f in listdir(path=args.input)]

        with Bar("Counting projects per CSV file... ", max=len(fileList)) as bar:
            file: Path
            for file in fileList:
                data["library"].append(file.stem)

                df: DataFrame = pandas.read_csv(filepath_or_buffer=file)
                dfgb: DataFrameGroupBy = groupByRepository(df=df)
                data["projectCount"].append(dfgb.ngroups)

                bar.next()

        df: DataFrame = DataFrame(data=data).sort_values(
            by="projectCount", ignore_index=True
        )

        df.to_csv(path_or_buf=args.output, index=False)

        plot(df=df, outputFilePath=args.fig)

    else:
        df: DataFrame = pandas.read_csv(filepath_or_buffer=args.input)
        dfgb: DataFrameGroupBy = groupByRepository(df=df)

        print(f"Project count: {dfgb.ngroups}")


if __name__ == "__main__":
    main()
