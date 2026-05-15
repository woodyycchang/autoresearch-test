# Toy in-memory "DB" using list of tuples

SCHEMA = ["id", "username", "email", "created_at", "last_login"]

USERS_DATA = [
    (1, "alice", "alice@example.com", "2024-01-01", None),
    (2, "bob", "bob@example.com", "2024-02-15", None),
]

def get_all_users():
    return USERS_DATA

def get_columns():
    return SCHEMA
