# Toy in-memory "DB" using list of tuples

SCHEMA = ["id", "username", "email", "created_at"]

USERS_DATA = [
    (1, "alice", "alice@example.com", "2024-01-01"),
    (2, "bob", "bob@example.com", "2024-02-15"),
]

def get_all_users():
    return USERS_DATA

def get_columns():
    return SCHEMA
