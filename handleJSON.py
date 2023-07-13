from pandas import DataFrame
import pandas
from argparse import ArgumentParser, Namespace


from os import listdir 
from pathlib import Path
from typing import List

import pandas
from progress.bar import Bar
from matplotlib import pyplot as plt

def getArgs()   ->  Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, required=True, help="Path to folder containing JSON files",)
    parser.add_argument("-o", "--output", required=True, help="A JSON file to dump data",)
    return parser.parse_args()


def main() -> None:
    args: Namespace = getArgs()

    dfList: List[DataFrame] = []
    jsonFiles: List[str] = listdir(path=args.input)

    with Bar("Reading JSON files to DataFrames... ", max=len(jsonFiles)) as bar:
        f: str
        for f in jsonFiles:
            filepath: Path = Path(args.input, f)
            df: DataFrame = pandas.read_json(path_or_buf=filepath, orient="index").reset_index()
            df.columns = ["repo", "calls"]
            dfList.append(df)
            bar.next()

    df: DataFrame = pandas.concat(objs=dfList, ignore_index=True)
    
    newDF: DataFrame = df.groupby(by=["repo"]).aggregate(func={"calls": "sum"}).reset_index()
    modelCount: int = newDF["repo"].size


    newDF.hist()
    plt.savefig("test.png")
    
    print(modelCount)

if __name__ == "__main__":
    main()
