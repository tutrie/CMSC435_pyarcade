def list_to_tuple(in_list: list, depth=1) -> tuple:
    if depth == 1:
        return tuple(in_list)

    for idx, lst in enumerate(in_list):
        in_list[idx] = list_to_tuple(lst, depth - 1)

    return tuple(in_list)


def json_tuple_decoder(json: dict, depth=1) -> dict:
    for key, value in json.items():
        if type(value) == list:
            json[key] = list_to_tuple(value, depth)

    return json
