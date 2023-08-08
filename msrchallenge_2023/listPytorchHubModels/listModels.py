from json import dump

from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, get


def downloadWebpage() -> BeautifulSoup:
    url: str = "https://pytorch.org/hub/research-models/compact"

    print(f"Downloading HTML content from {url}...")
    resp: Response = get(url=url)
    print("Downloaded HTML content")

    soup: BeautifulSoup = BeautifulSoup(markup=resp.content, features="lxml")
    return soup


def extractModelInformation(soup: BeautifulSoup) -> dict[str, str]:
    data: dict[str, str] = {}

    modelCards: ResultSet = soup.find_all(
        name="div",
        attrs={"class": "compact-model-card"},
    )

    card: Tag
    for card in modelCards:
        modelName: str = card.find(
            name="h4",
            attrs={"class": "compact-item-title"},
        ).text
        modelURL: str = f'https://pytorch.org{card.find(name="a").get(key="href")}'

        data[modelName] = modelURL

    return data


def main() -> None:
    soup: BeautifulSoup = downloadWebpage()
    modelInfo: dict[str, str] = extractModelInformation(soup=soup)

    with open("pytorchHubModels.json", "w") as jsonFile:
        dump(obj=modelInfo, fp=jsonFile, indent=4)


if __name__ == "__main__":
    main()
