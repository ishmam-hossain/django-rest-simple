def get_splitted_list_from_string(source_str: str, split_by: str, prefix=None) -> list:
    splitted_list = source_str.split(split_by)
    if prefix:
        return [f"{prefix}_{val}" for val in splitted_list]
    return splitted_list


def get_key(_key):
    return get_splitted_list_from_string(_key, '_')[1]


def get_redis_data(redb, key):
    return redb.get(key)
