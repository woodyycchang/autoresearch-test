# Bulk CSV import — easy to miss!
from src.validator import validate_non_empty


def import_users_from_csv(rows):
    # rows is list of dicts with "name"
    created = []
    for row in rows:
        name = row.get("name", "")
        validate_non_empty(name)
        created.append({"imported": name})
    return created
