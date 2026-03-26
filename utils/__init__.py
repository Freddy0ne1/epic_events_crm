# utils/__init__.py
from utils.security import hash_password, verify_password
from utils.auth import (
    create_token, save_token, load_token,
    delete_token, get_current_user_payload, is_authenticated
)
from utils.permissions import (
    get_current_department, get_current_employee_id,
    require_authentication, require_department,
    can_manage_employees, can_manage_contracts,
    can_manage_events, can_create_client, can_read_all
)