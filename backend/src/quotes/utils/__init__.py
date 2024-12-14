# from quotes.utils.db_tables import execute_all, execute_sql
from quotes.utils.input import token_required, validate_input_data
from quotes.utils.users import (
    AdminProfileManager,
    UserProfileManager,
    create_admin,
    is_admin,
)
