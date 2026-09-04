"""Tiferet MUI Core Assets."""

# *** imports

# ** app
from tiferet.assets.core import create_service_module_path

# *** constants (ids)

# ** constant: state_service_id
STATE_SERVICE_ID = 'state_service'

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
