conf_filename = '.todo.conf'

required_fields = [
    "secret"
]

optional_fields = {
    "show_inbox" : True
}

def validate_conf(conf_json):
    for required in required_fields:
        if required not in conf_json:
            raise ValueError(".todo.conf is missing {}".format(required))

    for optional in optional_fields:
        if optional not in conf_json:
            conf_json[optional] = optional_fields[optional]

    return conf_json
