from json import dump
from pathlib import Path
from typing import List

import click
from progress.bar import Bar
from timm.models import list_models
from timm.models._pretrained import PretrainedCfg
from timm.models._registry import get_pretrained_cfg


def getHFModels(modelNames: List[str]) -> dict[str, str | None]:
    data: dict[str, str | None] = {}

    with Bar(
        "Getting the Hugging Face ID of timm models... ", max=len(modelNames)
    ) as bar:
        name: str
        for name in modelNames:
            config: PretrainedCfg | None = get_pretrained_cfg(model_name=name)

            if config is None:
                data[name] = None
            else:
                data[name] = config.hf_hub_id

            bar.next()

    return data


@click.command()
@click.option(
    "outputJSON",
    "-o",
    "--output",
    nargs=1,
    type=Path,
    required=True,
    help="Path to JSON file to save data to",
)
def main(outputJSON) -> None:
    genericModels: List[str] = list_models(pretrained=False)
    pretrainedModels: List[str] = list_models(pretrained=True)

    models: List[str] = genericModels + pretrainedModels

    data: dict[str, str | None] = getHFModels(modelNames=models)

    with open(file=outputJSON, mode="w") as jsonFile:
        dump(obj=data, fp=jsonFile, indent=4)


if __name__ == "__main__":
    main()
