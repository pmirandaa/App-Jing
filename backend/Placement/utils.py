import copy


def sort_and_place(items, *, key, start=1, allow_ties=True):
    def get_key(item):
        if isinstance(key, str):
            return item[key] if key[0] != "-" else -item[key[1:]]
        elif callable(key):
            return key(item)
        elif isinstance(key, tuple) or isinstance(key, list):
            keys = []
            for k in key:
                if isinstance(k, str):
                    keys.append(item[k] if k[0] != "-" else -item[k[1:]])
                elif callable(k):
                    keys.append(k(item))
                else:
                    raise TypeError(
                        'key must be a string, callable or list of strings or callables')
            return keys
        else:
            raise TypeError(
                'key must be a string, callable or list of strings or callables')

    if not isinstance(items, list):
        raise TypeError('items must be a list')
    if len(items) == 0:
        return items

    items_copy = copy.deepcopy(items)
    sorted_items = sorted(items_copy, key=get_key, reverse=True)

    if allow_ties:
        place_current = start
        value_current = get_key(sorted_items[0])
        for i, item in enumerate(sorted_items, start=start):
            this_key = get_key(item)
            if this_key == value_current:
                item['place'] = place_current
            else:
                item['place'] = i
                place_current = i
                value_current = this_key
    else:
        for i, item in enumerate(sorted_items, start=start):
            item['place'] = i

    return sorted_items
