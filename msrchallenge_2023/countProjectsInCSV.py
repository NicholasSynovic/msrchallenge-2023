from argparse import ArgumentParser, Namespace
from typing import Path

import pandas
from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Path to CSV file to count repositories",
    )
    return parser.parse_args()


def groupByRepository(df: DataFrame) -> DataFrameGroupBy:
    dfgb: DataFrameGroupBy = df.groupby(by=["repository"])
    return dfgb


def main() -> None:
    args: Namespace = getArgs()

    df: DataFrame = pandas.read_csv(filepath_or_buffer=args.input)

    dfgb: DataFrameGroupBy = groupByRepository(df=df)

    print(f"Project count: {dfgb.ngroups}")


if __name__ == "__main__":
    main()
