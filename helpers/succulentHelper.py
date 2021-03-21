def is_valid_succulent(body):
    attrs = ["name", "family_id"]

    for attr in attrs:
        if attr not in body or body[attr] is None:
            return False

    return True
