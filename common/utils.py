from ast import literal_eval

from common import redb


def get_common_prefix_redis_keys(prefix: str):
    return redb.scan_iter(f"{prefix}*")


def string_splitter(source_str: str, split_by: str, prefix: str = None) -> list:
    split_list = source_str.split(split_by)
    if prefix:
        return [f"{prefix}:{val}" for val in split_list]
    return split_list


def get_key(key: str) -> str:
    return string_splitter(key, ':')[1]


def get_redis_data(key: str):
    return redb.get(key)


def isiterable(val):
    if isinstance(val, dict) or isinstance(val, list):
        return True
    return


def set_redis_iterable_data(key: str, value):
    return redb.set(key, str(value))


def set_redis_data(key: str, value):
    if isiterable(value):
        return set_redis_iterable_data(key, value)
    return redb.set(key, value)


def key_in_redis(key: str) -> bool:
    return redb.exists(key) == 1


def set_ttl(key: str, time_to_live: int = 5):
    return redb.expire(key, time_to_live)


def reset_ttl(key: str):
    return set_ttl(key)


def string_to_dict(data: bytes):
    return literal_eval(data.decode())


def get_response_and_reset_ttl(all_keys: list):
    _response = dict()
    _not_found = []

    for key in all_keys:
        key_data = get_redis_data(key)

        if key_data:
            _response[get_key(key)] = key_data
        else:
            _not_found.append(get_key(key))

        reset_ttl(key)

    return _response, _not_found
