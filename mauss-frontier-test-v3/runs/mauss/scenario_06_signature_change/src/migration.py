from src.user import User

# Migrates a batch of users with multiple roles each
def migrate_batch(records):
    users = []
    for rec in records:
        u = User(rec["name"])
        u.add_roles(rec["roles"])
        users.append(u)
    return users
