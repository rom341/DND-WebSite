import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'projects', 'dndsite'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dndsite.settings')

import django
django.setup()


from tests.fixtures import (
    use_fast_password_hasher,
    client,
    user_credentials_admin,
    user_credentials_player,
    default_test_users_list,
    default_test_characters_list,
    default_test_roles_list,
    default_test_lobbys_list,
    default_test_locations_list,
    user_admin,
    user_player,
    auth_client_admin,
    auth_client_player
)
