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
def main(modelName: str, usePTM: bool) -> None:
    print(modelName, usePTM)


if __name__ == "__main__":
    main()
