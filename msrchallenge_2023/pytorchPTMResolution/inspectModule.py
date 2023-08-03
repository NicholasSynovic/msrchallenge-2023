import inspect
from enum import EnumMeta
from types import MappingProxyType, ModuleType
from typing import Any, List, Tuple

import torchvision.models
import torchvision.models.detection
import torchvision.models.optical_flow
import torchvision.models.quantization
import torchvision.models.segmentation
import torchvision.models.video
from pandas import DataFrame
from progress.bar import Bar


def getListOfWeights(module: Any) -> List[EnumMeta]:
    data: List[EnumMeta] = []
    tempData = inspect.getmembers(module, inspect.isclass)

    with Bar(f"Extracting weight instances from module... ", max=len(tempData)) as bar:
        for name, class_ in tempData:
            if "_Weights" in name:
                data.append(class_)
            bar.next()

    return data


def extractInformation(weightClass: List[EnumMeta]) -> List[dict]:
    data: List[dict] = []

    with Bar("Extracting class information... ", max=len(weightClass)) as bar:
        class_: EnumMeta
        for class_ in weightClass:
            json: dict[str, str | List[dict[str, str]]] = {
                "Model Name": "",
                "Weights": [],
            }

            json["Model Name"] = class_.__name__.split(sep="_Weights")[0]

            members: MappingProxyType = class_.__members__

            key: str
            for key in members.keys():
                foo: dict[str, str] = {"Name": "", "Alias": "", "URL": ""}

                foo["Name"] = key.__str__()
                foo["Alias"] = members[key].__str__()
                foo["URL"] = getattr(class_, key).url

                json["Weights"].append(foo)

            data.append(json)
            bar.next()

    return data


def main() -> None:
    models: ModuleType = torchvision.models
    quantization: ModuleType = torchvision.models.quantization
    detection: ModuleType = torchvision.models.detection
    segmentation: ModuleType = torchvision.models.segmentation
    video: ModuleType = torchvision.models.video
    opticalFlow: ModuleType = torchvision.models.optical_flow

    weightClass_Models: List[EnumMeta] = getListOfWeights(module=models)
    weightClass_Detection: List[EnumMeta] = getListOfWeights(module=detection)
    weightClass_Video: List[EnumMeta] = getListOfWeights(module=video)
    weightClass_Quantization: List[EnumMeta] = getListOfWeights(
        module=quantization,
    )
    weightClass_Segmentation: List[EnumMeta] = getListOfWeights(
        module=segmentation,
    )
    weightClass_OpticalFlow: List[EnumMeta] = getListOfWeights(
        module=opticalFlow,
    )

    metadata_Models: List[dict] = extractInformation(
        weightClass=weightClass_Models,
    )
    metadata_Detection: List[dict] = extractInformation(
        weightClass=weightClass_Models,
    )
    metadata_Video: List[dict] = extractInformation(
        weightClass=weightClass_Models,
    )
    metadata_Quantization: List[dict] = extractInformation(
        weightClass=weightClass_Models,
    )
    metadata_Segmentation: List[dict] = extractInformation(
        weightClass=weightClass_Models,
    )
    metadata_OpticalFlow: List[dict] = extractInformation(
        weightClass=weightClass_Models,
    )


if __name__ == "__main__":
    main()
