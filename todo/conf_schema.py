import os
import json


class Config:
    def __init__(self, conf_json, required, optional):
        self.required_fields = required
        self.optional_fields = optional
        self.conf_json = self.validate_conf(conf_json)

    def validate_conf(self, conf_json):
        for required in self.required_fields:
            if required not in conf_json:
                raise ValueError(".todo.conf is missing {}".format(required))

        for optional in self.optional_fields:
            if optional not in conf_json:
                conf_json[optional] = self.optional_fields[optional]

        return conf_json

    def __getitem__(self, key):
        return self.conf_json[key]

    def __setitem__(self, key, value):
        self.conf_json[key] = value


class TodoConfig(Config):
    def __init__(self, conf_json, required, optional):
        super().__init__(conf_json, required, optional)

    @staticmethod
    def get_config():
        conf_filename = '.todo.json'

        required_fields = [
            "secret"
        ]

        # Optional fields paired with their default value.
        optional_fields = {
            "show_inbox": True,
            "default_project": None
        }

        conf_filepath = os.path.join(os.path.expanduser('~'), conf_filename)
        with open(conf_filepath) as conf_file:
            conf_json = json.load(conf_file)
            return TodoConfig(conf_json, required_fields, optional_fields)
