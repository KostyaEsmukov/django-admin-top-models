

def list_get_or_default(list, idx, default):
    try:
        return list[idx]
    except IndexError:
        return default
