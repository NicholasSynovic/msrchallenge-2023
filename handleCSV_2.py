from pandas import DataFrame, Series
import pandas
# from pprint import pprint as print
from typing import Hashable
from pandas.core.groupby.generic import DataFrameGroupBy
from progress.bar import Bar


def strReplacement(series: Series)   ->  Series:
    series = series.str.replace(
            r"[^a-zA-Z0-9\-\_\/]",
            "",
            regex=True,
            )

    return series

def groupByRepository(df: DataFrame)    ->  DataFrameGroupBy:
    dfgb: DataFrameGroupBy = df.groupby(by=["repository"])
    return dfgb


def countDynamicModelUsageRepositories(dfgb: DataFrameGroupBy)  ->  tuple[int, int, int, int, float, float, float, float]:
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

            bar.next()


    percentDynamicUsage: float = (dynamicUsageRepos / totalNumberOfRepos) * 100
    percentStaticUsage: float = (staticUsageRepos / totalNumberOfRepos) * 100
    percentPureStaticUsage_total: float = (pureStaticUsageRepos / totalNumberOfRepos) * 100
    percentPureStaticUsage_partial: float = (pureStaticUsageRepos / staticUsageRepos) * 100

    return (totalNumberOfRepos, dynamicUsageRepos, staticUsageRepos, pureStaticUsageRepos, percentDynamicUsage, percentStaticUsage, percentPureStaticUsage_total, percentPureStaticUsage_partial,)

def main()  ->  None:
    csvFile: str = "githubRepositoriesThatUseTransformersLibrary.csv"

    df: DataFrame = pandas.read_csv(filepath_or_buffer=csvFile)

    df["param_hardcoded"] = strReplacement(series=df["param_hardcoded"])

    dfgb: DataFrameGroupBy = groupByRepository(df=df)
    
    data: tuple[int, int, int, float, float] = countDynamicModelUsageRepositories(dfgb=dfgb)

    print(data)


if __name__ == "__main__":
    main()
