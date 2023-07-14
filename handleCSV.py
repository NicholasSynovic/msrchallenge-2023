from os import mkdir
from pathlib import Path
from typing import List

import pandas
from pandas import DataFrame, Series
from pandas.io.parsers.readers import TextFileReader
from progress.bar import Bar
from progress.spinner import Spinner
from argparse import ArgumentParser, Namespace
from json import dump
from pprint import pprint as print

def splitCSV(tfr: TextFileReader, outputDir: Path) -> None:
    try:
        mkdir(path=outputDir)
    except FileExistsError:
        pass

    counter: int = 0

    with Spinner(f"Splitting CSV into chunks stored in ./{outputDir}... ") as spinner:
        df: DataFrame
        for df in tfr:
            path: Path = Path(outputDir, str(counter) + ".csv")
            df.to_csv(path_or_buf=path, index=False)
            counter += 1

            spinner.next()


def extractRelevantInformation(df: DataFrame) -> DataFrame:
    df.drop(
        ["repository", "match", "from_or_import", "method", "file"],
        axis=1,
        inplace=True,
    )
    return df


def readModelList(filePath: str) -> List[str]:
    with open(file=filePath) as file:
        lines: List[str] = file.readlines()
        file.close()

    lines: List[str] = [line.strip().replace('"', "") for line in lines]
    return lines


def countContainedModels(
    df: DataFrame,
    modelList: List[str],
    message: str,
    maxBarLen: int,
) -> dict[str, int]:
    data: dict[str, int] = {}

    with Bar(message, max=maxBarLen) as bar:
        model: str
        for model in modelList:
            validRows: DataFrame = df[df["param_hardcoded"].str.contains(model) == True]

            if validRows.empty:
                bar.next()
                continue

            relevantColumn: Series = validRows["param_hardcoded"]
            exactData: Series = relevantColumn == model
            exactData: Series = exactData[exactData]

            if exactData.empty:
                bar.next()
                continue

            data[model] = len(exactData)
            bar.next()

    return data

def getArgs()   ->  Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="A CSV file to read",)
    parser.add_argument("-o", "--output", required=True, help="A JSON file to dump data",)
    return parser.parse_args()


def main() -> None:
    args: Namespace = getArgs()

    modelListFile: str = "ptmTorrentV1FileList.txt"

    modelList: List[str] = readModelList(filePath=modelListFile)
    modelListLength: int = len(modelList)

    # largeCSV: str = "githubRepositoriesThatUseTransformersLibrary.csv"
    # tfr: TextFileReader = pandas.read_csv(filepath_or_buffer=largeCSV, chunksize=1000)
    # largeCSVSplitOutputDir: Path = Path("csvStorage")
    # splitCSV(tfr=tfr, outputDir=largeCSVSplitOutputDir)

    # df: DataFrame
    # for df in tfr:
    df: DataFrame = pandas.read_csv(filepath_or_buffer=args.input)
    df: DataFrame = extractRelevantInformation(df=df)

    print(df["param_hardcoded"].to_list())
    quit()

    df["param_hardcoded"] = df["param_hardcoded"].str.replace(
        r"[^a-zA-Z0-9-/]",
        "",
        regex=True,
    )

    data: dict[str, int] = countContainedModels(
        df,
        modelList,
        message=f"Counting models used in {args.input} ...",
        maxBarLen=modelListLength,
    )

    with open(args.output, "w") as output:
        dump(obj=data, fp=output, indent=4)
        output.close()


if __name__ == "__main__":
    main()
