from pandas import DataFrame
from progress.spinner import Spinner
from pandas.io.parsers.readers import TextFileReader
import pandas
from os import mkdir
from pathlib import Path

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


def main()  ->  None:
    largeCSVSplitOutputDir: Path = Path("csvStorage")

    tfr: TextFileReader = pandas.read_csv(filepath_or_buffer="githubRepositoriesThatUseTransformersLibrary.csv", chunksize=1000)

    splitCSV(tfr=tfr, outputDir=largeCSVSplitOutputDir)


if __name__ == "__main__":
    main()
