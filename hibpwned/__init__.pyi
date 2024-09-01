"""__init__.pyi"""

from __future__ import annotations
import requests

ReturnAlias = int | list[dict[str, str | int | bool]]

AltReturnAlias = int | list[dict[str, str | int | bool]] | list[str]

DataAlias = list[dict[str, str | int | bool]] | dict[str, str | int | bool]

AltDataAlias = (list[dict[str, str | int | bool]]
                | dict[str, str | int | bool] | list[str])


def _check(resp: requests.models.Response) -> None:
    ...


class Pwned:

    url: str
    resp: requests.models.Response
    truncate_string: str
    domain_string: str
    unverified_string: str
    classes: list[str]
    hashes: str
    hash_list: list[str]
    hexdig: str
    hsh: str
    pnum: str
    data: DataAlias
    alt_data: AltDataAlias

    def __init__(self, account: str, agent: str, key: str) -> None:
        ...

    def search_all_breaches(self,
                            truncate: bool | None = False,
                            domain: str | None = None,
                            unverified: bool | None = False) -> AltReturnAlias:
        ...

    def all_breaches(self, domain: str | None = None) -> ReturnAlias:
        ...

    def single_breach(self, name: str) -> ReturnAlias:
        ...

    def data_classes(self) -> int | list[str]:
        ...

    def search_pastes(self) -> ReturnAlias:
        ...

    def search_password(self, password: str) -> int | str:
        ...

    def search_hashes(self, hsh: str) -> int | str:
        ...
