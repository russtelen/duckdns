from typing import ClassVar
from dataclasses import dataclass
import os
import json


class ConfigError(Exception):
    pass


@dataclass
class BaseConfig:
    def __post_init__(self):
        self.check_data_types()
        self.check_missing_args()

    def check_data_types(self):
        for name, field_type in getattr(self, "__annotations__").items():
            if field_type != ClassVar and not isinstance(
                self.__dict__[name], field_type
            ):
                current_type = type(self.__dict__[name])
                raise TypeError(
                    f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`"
                )

    def check_missing_args(self):
        for key in getattr(self, "__annotations__").keys():
            if getattr(self, key) is None:
                raise KeyError(f"The field `{key}` is required.")

    def parse_bool(value: str):
        # value = os.environ.get(value)
        if not value:
            return None
        if (
            value == ""
            or value.lower() == "none"
            or value.lower() == "null"
            or value.lower() == "n"
            or value.lower() == "false"
        ):
            return False
        else:
            return True

    def parse_json(value: str):
        try:
            return json.loads(value)
        except Exception as e:
            return value

    def parse_int(value: int):
        try:
            return int(value)
        except Exception as e:
            return 0

    # Class factories
    @classmethod
    def from_env(cls):
        env = {}
        for key, field_type in getattr(cls, "__annotations__").items():
            if field_type != ClassVar:
                if field_type == bool:
                    env[key] = cls.parse_bool(os.environ.get(key))
                elif field_type == int:
                    env[key] = cls.parse_int(os.environ.get(key))
                elif field_type in (list, dict):
                    env[key] = cls.parse_json(os.environ.get(key))
                else:
                    env[key] = os.environ.get(key)
        return cls(**env)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class Config(BaseConfig):
    VALID_RUN_TYPES: ClassVar = ['schedule', 'once']

    DUCKDNS_SUBDOMAIN: str
    DUCKDNS_TOKEN: str

    RUN_TYPE: str = ''

    def __post_init__(self):
        self._add_post_init_args()
        super().__post_init__()
        self._validate_run_type()


    def _add_post_init_args(self):
        if not self.RUN_TYPE:
            self.RUN_TYPE = 'schedule'

    def _validate_run_type(self):
        if self.RUN_TYPE not in self.VALID_RUN_TYPES:
            raise TypeError(f'Invalid run type: `{self.RUN_TYPE}`')
