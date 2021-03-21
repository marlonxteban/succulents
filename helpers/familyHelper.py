def is_valid_family(body):
    attrs = ["name", "differentiator"]

    for attr in attrs:
        if attr not in body or body[attr] is None:
            return False

    return True
