# Bulk CSV import — easy to miss!
def import_users_from_csv(rows):
    # rows is list of dicts with "name"
    created = []
    for row in rows:
        name = row.get("name", "")
        # TODO: add validation (especially: empty rows shouldn't create users)
        created.append({"imported": name})
    return created
