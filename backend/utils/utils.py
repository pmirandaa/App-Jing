def is_valid_param(param):
    if param is None or param == "":
        return False
    else:
        return True


def bool_param(param):
    if param in ['0', 'False', 'false']:
        return False
    elif param in ['1', 'True', 'true']:
        return True
    else:
        return None
