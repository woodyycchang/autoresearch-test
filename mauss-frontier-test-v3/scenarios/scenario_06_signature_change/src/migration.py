from src.user import User

# Migrates a batch of users with multiple roles each
def migrate_batch(records):
    users = []
    for rec in records:
        u = User(rec["name"])
        for r in rec["roles"]:
            u.add_role(r)
        users.append(u)
    return users
