from argparse import ArgumentParser, Namespace
from os import listdir
from os.path import isdir
from pathlib import Path
from typing import Hashable, List

import pandas
from pandas import DataFrame, Series
from pandas.core.groupby.generic import DataFrameGroupBy
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


def strReplacement(series: Series) -> Series:
    try:
        series = series.str.replace(
            r"[^a-zA-Z0-9\-\_\/]",
            "",
            regex=True,
        )
    except AttributeError:
        pass

    return series


def groupByRepository(df: DataFrame) -> DataFrameGroupBy:
    dfgb: DataFrameGroupBy = df.groupby(by=["repository"])
    return dfgb


def countDynamicModelUsageRepositories(
    dfgb: DataFrameGroupBy,
) -> tuple[int, int, int, int, float, float, float, float]:
    """
    Returns a tuple in this order:
        [
            # of Repositories (total)
            # of Dynamic Usage Repositories,
            # of Static Usage Repositories where at least 1 file uses a static call,
            # of Pure Static Usage Repositories
            # Percent Dynamic Usage,
            # Percent Static Usage,
            # Percent Pure Static Usage against total,
            # Percent Pure Static Usage against partial static,
        ]
    """

    top5Repos: DataFrame = DataFrame(data={"project": [], "count": []})

    totalNumberOfRepos: int = dfgb.ngroups
    dynamicUsageRepos: int = 0
    staticUsageRepos: int = 0
    pureStaticUsageRepos: int = 0

    with Bar("Counting dynamic usage repositories... ", max=dfgb.ngroups) as bar:
        pair: tuple[Hashable, DataFrame]
        for pair in dfgb:
            countNaN: int = 0
            countValid: int = 0

            df: DataFrame = pair[1]

            countNaN = df["param_hardcoded"].isna().sum()
            countValid = df["param_hardcoded"].size - countNaN

            if countValid >= 1:
                staticUsageRepos += 1
            else:
                dynamicUsageRepos += 1

            if (countValid >= 1) and (countNaN == 0):
                pureStaticUsageRepos += 1

            top5Repos.loc[-1] = (df["repository"].iloc[0], countNaN)
            top5Repos.index = top5Repos.index + 1
            top5Repos.sort_index()

            bar.next()

    # top5Repos.sort_values(by="count", ignore_index=True, inplace=True)
    # top5Repos.to_csv(path_or_buf="projectOrderByDynamicModelUsage.csv", index=False)

    percentDynamicUsage: float = (dynamicUsageRepos / totalNumberOfRepos) * 100
    percentStaticUsage: float = (staticUsageRepos / totalNumberOfRepos) * 100
    percentPureStaticUsage_total: float = (
        pureStaticUsageRepos / totalNumberOfRepos
    ) * 100

    try:
        percentPureStaticUsage_partial: float = (
            pureStaticUsageRepos / staticUsageRepos
        ) * 100
    except ZeroDivisionError:
        percentPureStaticUsage_partial: float = 0

    return (
        totalNumberOfRepos,
        dynamicUsageRepos,
        staticUsageRepos,
        pureStaticUsageRepos,
        percentDynamicUsage,
        percentStaticUsage,
        percentPureStaticUsage_total,
        percentPureStaticUsage_partial,
    )


def main() -> None:
    args: Namespace = getArgs()

    if isdir(s=args.input):
        dataDict: dict[str, List[str | int | float]] = {
            "library": [],
            "projectCount": [],
            "dynamicUsageCount": [],
            "patialStaticUsageCount": [],
            "pureStaticUsageCount": [],
            "percentDynamicUsage": [],
            "percentPartialStaticUsage": [],
            "percentPureStaticUsage_partial": [],
            "percentPureStaticUsage_total": [],
        }

        fileList: List[Path] = [Path(args.input, f) for f in listdir(path=args.input)]

        file: Path
        for file in fileList:
            dataDict["library"].append(file.stem)

            df: DataFrame = pandas.read_csv(filepath_or_buffer=file)
            df["param_hardcoded"] = strReplacement(series=df["param_hardcoded"])
            dfgb: DataFrameGroupBy = groupByRepository(df=df)

            data: tuple[
                int, int, int, int, float, float, float, float
            ] = countDynamicModelUsageRepositories(dfgb=dfgb)

            dataDict["projectCount"].append(data[0])
            dataDict["dynamicUsageCount"].append(data[1])
            dataDict["patialStaticUsageCount"].append(data[2])
            dataDict["pureStaticUsageCount"].append(data[3])
            dataDict["percentDynamicUsage"].append(data[4])
            dataDict["percentPartialStaticUsage"].append(data[5])
            dataDict["percentPureStaticUsage_partial"].append(data[6])
            dataDict["percentPureStaticUsage_total"].append(data[7])

        df: DataFrame = DataFrame(data=dataDict).sort_values(
            by="projectCount", ignore_index=True
        )

        df.to_csv(path_or_buf=args.output, index=False)

    else:
        csvFile: str = args.input
        df: DataFrame = pandas.read_csv(filepath_or_buffer=csvFile)
        df["param_hardcoded"] = strReplacement(series=df["param_hardcoded"])
        dfgb: DataFrameGroupBy = groupByRepository(df=df)
        data: tuple[
            int, int, int, int, float, float, float, float
        ] = countDynamicModelUsageRepositories(dfgb=dfgb)
        print(data)


if __name__ == "__main__":
    main()
