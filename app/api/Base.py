from dataclasses import dataclass
import requests


class APIError(Exception):
    ...


@dataclass
class BaseAPI:
    url: str = None

    def get(self, params: str = '', query: dict = None, headers: dict = None) -> str:
        url = f'{self.url}' + params
        res = requests.get(url, params=query, headers=headers)
        if res.status_code >= 400:
            raise APIError(f"API Error: {res.text}")
        return res

    def post(self, data: dict = None, params: str = '', query: dict = None, headers: dict = None) -> str:
        url = f'{self.url}' + params
        res = requests.post(url, json=data, params=query, headers=headers)
        if res.status_code >= 400:
            raise APIError(f"API Error: {res.text}")
        return res
