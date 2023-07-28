import logging
from pathlib import Path

import click
import timm


@click.command()
@click.option(
    "modelName",
    "-i",
    "--input",
    nargs=1,
    type=str,
    required=True,
    help="Model to test",
)
@click.option(
    "usePTM",
    "-p",
    "--load-pretrained-weights",
    is_flag=True,
    help="Load pretrained weights of the model",
)
@click.option(
    "logFile",
    "-l",
    "--log-file",
    type=Path,
    nargs=1,
    required=True,
    help="Path to file to save timm debug logs to",
)
def main(modelName: str, usePTM: bool, logFile: Path) -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        filename=logFile,
    )

    timm.create_model(model_name=modelName, pretrained=usePTM)


if __name__ == "__main__":
    main()
