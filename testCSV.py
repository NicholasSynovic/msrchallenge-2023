import pandas
import time

csvFile: str = "githubRepositoriesThatUseTransformersLibrary.csv"

start = time.time_ns()
pandas.read_csv(filepath_or_buffer=csvFile)
end = time.time_ns()

print(end - start)
