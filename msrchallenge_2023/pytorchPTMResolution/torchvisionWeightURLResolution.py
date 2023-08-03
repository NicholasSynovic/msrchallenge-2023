from typing import List, Tuple


def readFile() -> List[str]:
    with open("pytorchWeightsList.txt", "r") as txtFile:
        data: List[str] = [line.strip() for line in txtFile.readlines()]
        txtFile.close()
    return data


def extractQuantizedWeights(data: List[str]) -> Tuple[List[str], List[str]]:
    weights: List[str] = []
    quantizedWeights: List[str] = []

    weightName: str
    for weightName in data:
        if "_QuantizedWeights" in weightName:
            quantizedWeights.append(weightName)
        else:
            weights.append(weightName)

    return (quantizedWeights, weights)


def importClasses(
    data: List[str],
    moduleName: str = "torchvision.models",
) -> None:
    className: str
    for className in data:
        __import__(name=moduleName, fromlist=[className])


def main() -> None:
    weightData: List[str] = readFile()[1::]

    quantizedWeights, weights = extractQuantizedWeights(data=weightData)


if __name__ == "__main__":
    main()
