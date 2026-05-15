from src.queries import select_all_users_as_dicts, select_user_email_by_id

def find_email(user_id):
    return select_user_email_by_id(user_id)

def all_users():
    return select_all_users_as_dicts()
