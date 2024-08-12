from json import dumps
from typing import Optional

from fastapi.testclient import TestClient


class BaseClient:
    def __init__(self, client: TestClient, endpoint_path: str):
        self.client = client
        self.path = endpoint_path
        self.headers = {"content-type": "application/json"}
        self.client.headers.update(self.headers)

    def get_by_id(self, id: int | str):
        return self.client.get(f"/{self.path}/{id}")

    def get_all(self, **kwargs):
        return self.client.get(f"/{self.path}/", params=kwargs)

    def get_paginated(self, **kwargs):
        return self.client.get(f"/{self.path}/", params=kwargs)

    def create(self, data: dict | list, headers: Optional[dict] = None):
        if type(data) in [dict, list]:
            data = dumps(data)
        return self.client.request(
            "POST", f"/{self.path}/", content=data, headers=headers
        )

    def update(self, id: int | str, data: dict | list, headers: Optional[dict] = None):
        if type(data) in [dict, list]:
            data = dumps(data)
        return self.client.request(
            "PUT", f"/{self.path}/{id}", content=data, headers=headers
        )

    def patch(self, id: int, data: dict | list, headers: Optional[dict] = None):
        if type(data) in [dict, list]:
            data = dumps(data)
        return self.client.request(
            "PATCH", f"/{self.path}/{id}", content=data, headers=headers
        )

    def put(self, id: int, data: dict | list, headers: Optional[dict] = None):
        if type(data) in [dict, list]:
            data = dumps(data)
        return self.client.request(
            "PUT", f"/{self.path}/{id}", content=data, headers=headers
        )

    def delete(self, id: int | str):
        return self.client.delete(f"/{self.path}/{id}")
