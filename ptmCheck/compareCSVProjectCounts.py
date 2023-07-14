from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy
import pandas

def groupByRepository(df: DataFrame) -> DataFrameGroupBy:
    dfgb: DataFrameGroupBy = df.groupby(by=["repository"])
    return dfgb


def main()  ->  None:
    transformersFilePath: str = "githubRepositoriesThatUseTransformersLibrary.csv"
    spacyFilePath: str = "githubRepositoriesThatUseSpacyLibrary.csv"

    transformersDF: DataFrame = pandas.read_csv(filepath_or_buffer=transformersFilePath)
    spacyDF: DataFrame = pandas.read_csv(filepath_or_buffer=spacyFilePath)

    transformersDFGB: DataFrameGroupBy = groupByRepository(df=transformersDF)
    spacyDFGB: DataFrameGroupBy = groupByRepository(df=spacyDF)

    print(f"Projects that use Transformers: {transformersDFGB.ngroups}")
    print(f"Projects that use Spacy:        {spacyDFGB.ngroups}")

    pass

if __name__ == "__main__":
    main()
