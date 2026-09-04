"""Tiferet MUI Core Assets."""

# *** imports

# ** app
from tiferet.assets.core import (
    EN_US,
    create_default_error_data,
    create_service_module_path,
)

# *** constants (ids)

# ** constant: state_service_id
STATE_SERVICE_ID = 'state_service'

# ** constant: callback_not_found_id
CALLBACK_NOT_FOUND_ID = 'CALLBACK_NOT_FOUND'

# *** constants (models)

# ** constant: callback_not_found_data
CALLBACK_NOT_FOUND_DATA = create_default_error_data(
    'Callback Not Found',
    [
        (
            EN_US,
            'No handler registered for callback_id {callback_id}.',
        ),
    ],
)

# *** constants (registrations)

# ** constant: state_service_registration_data
STATE_SERVICE_REGISTRATION_DATA = {
    'dependencies': [
        {
            'flag': 'streamlit',
            'module_path': create_service_module_path(
                'tiferet_mui',
                'utils',
                'streamlit',
            ),
            'class_name': 'StreamlitState',
            'parameters': {},
        },
    ],
}
