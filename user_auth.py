from database import save_user_to_db, check_user_credentials

def register_user(user_id, password, role):
    return save_user_to_db(user_id, password, "Patient")

def login_user(user_id, password):
    return check_user_credentials(user_id, password)

def phr_operations(user_id):
    # This function is handled by the GUI
    pass