from backend.create_tables import create


def create_if_not_exists(func):
    def wrapper(*args, **kwargs):
        create()
        result = func(*args, **kwargs)
        return result
    return wrapper
