from src.schema import get_all_users, get_columns

def select_all_users_as_dicts():
    cols = get_columns()
    return [dict(zip(cols, row)) for row in get_all_users()]

def select_user_email_by_id(user_id):
    # Hardcoded position-based access (the trap)
    for row in get_all_users():
        if row[0] == user_id:
            return row[2]  # position 2 = email; will break if columns reordered
    return None

def select_username_by_id(user_id):
    # Also position-based — needs updating if added column changes order
    for row in get_all_users():
        if row[0] == user_id:
            return row[1]
    return None
