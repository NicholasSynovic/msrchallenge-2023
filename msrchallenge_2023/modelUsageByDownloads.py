from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List, Tuple

import pandas
from matplotlib import pyplot as plt
from pandas import DataFrame, Series
from progress.bar import Bar


def getArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--csv",
        required=True,
        help="CSV containing information",
        type=Path,
    )
    parser.add_argument(
        "--json",
        required=True,
        help="JSON containing information",
        type=Path,
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Path to save the output figure",
        type=Path,
    )
    return parser.parse_args()


def extractRelevantData(df: DataFrame, relevantModels: Series) -> Series:
    df.dropna(subset=["param_hardcoded"], ignore_index=True, inplace=True)
    allModels: Series = df["param_hardcoded"]

    try:
        allModels = allModels.str.replace(
            r"[^a-zA-Z0-9\-\_\/]",
            "",
            regex=True,
        )
    except AttributeError:
        pass

    mask: Series = allModels.isin(values=relevantModels)

    allModels.mask(cond=~mask, inplace=True)
    data: Series = allModels.dropna(ignore_index=True)

    return data


def getDownloadsPerModel(models: Series, modelMetadata: DataFrame) -> DataFrame:
    dfList: List[DataFrame] = []
    columns: List[str] = ["model", "downloads"]

    allModels: Series = modelMetadata["context_id"]
    modelMask: Series = allModels.isin(values=models)

    allModels.mask(cond=~modelMask, inplace=True)
    relevantModels: Series = allModels.dropna(ignore_index=True)

    with Bar("Getting downloads for models... ", max=relevantModels.size) as bar:
        model: str
        for model in relevantModels:
            mask: DataFrame = modelMetadata["context_id"] == model
            downloads: int = modelMetadata[mask]["downloads"].iloc[0]
            df: DataFrame = DataFrame(data=[[model, downloads]], columns=columns)
            dfList.append(df)
            bar.next()

    df: DataFrame = pandas.concat(objs=dfList, ignore_index=True)
    return df


def groupBy(df: DataFrame, values: List[Tuple[int, int]]) -> List[DataFrame]:
    dfList: List[DataFrame] = []

    with Bar("Creating groups... ", max=len(values)) as bar:
        pair: Tuple[int, int]
        for pair in values:
            minValue: int = pair[0]
            maxValue: int = pair[1]
            tempDF: DataFrame = df[
                (df["downloads"] >= minValue) & (df["downloads"] < maxValue)
            ]
            dfList.append(tempDF)
            bar.next()

    return dfList


def plot(dfs: List[DataFrame], xAxis_Groups: List[Tuple[int, int]], output: Path,) -> None:
    pairs: List[Tuple[Tuple[int, int], DataFrame]] = list(zip(xAxis_Groups, dfs))

    data: dict[str, int] = {
        f"{key[0]} - {key[1]}": value.shape[0] for (key, value) in pairs
    }

    plt.bar(*zip(*data.items()))

    plt.ylabel(ylabel="# of Models")
    plt.xlabel(xlabel="Download Range")
    plt.xticks(rotation=45, ha="right", fontsize="x-small")
    plt.title(label="# of Models Used in Projects vs Downloads")

    ax = plt.gca()
    for bar in ax.patches:
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
    plt.savefig(output)


def main() -> None:
    args: Namespace = getArgs()

    GROUPING_VALUES: List[Tuple[int, int]] = [
        (0, 10),
        (10, 100),
        (100, 1000),
        (1000, 10000),
        (10000, 100000),
        (100000, 1000000),
        (1000000, 10000000000),
    ]

    print(f"Reading {args.json}...")
    jsonDF: DataFrame = pandas.read_json(path_or_buf=args.json)

    print(f"Reading {args.csv}...")
    csvDF: DataFrame = pandas.read_csv(filepath_or_buffer=args.csv)

    print("Extracting relevant model information...")
    relevantModels: Series = extractRelevantData(
        df=csvDF,
        relevantModels=jsonDF["context_id"],
    )

    df: DataFrame = getDownloadsPerModel(models=relevantModels, modelMetadata=jsonDF)

    groups: List[DataFrame] = groupBy(df=df, values=GROUPING_VALUES)

    print(f"Saving figure to {args.output}...")
    plot(dfs=groups, xAxis_Groups=GROUPING_VALUES, output=args.output)


if __name__ == "__main__":
    main()
