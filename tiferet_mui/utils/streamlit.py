"""Streamlit-specific Tiferet MUI utilities."""

# *** imports

# ** core
from pathlib import Path
from typing import Any

# ** infra
import streamlit as st

# ** app
from ..interfaces import StateService

# *** functions

# ** function: get_streamlit_bundle_path
def get_streamlit_bundle_path() -> str:
    '''
    Return the absolute filesystem path of the vendored Streamlit bundle.

    Keeping the asset location beside this host-specific adapter lets the
    Streamlit blueprint declare the component without embedding a path.

    :return: The vendored component bundle path.
    :rtype: str
    '''

    # Resolve the package-relative frontend bundle for Streamlit's path API.
    return str(Path(__file__).parents[1] / 'assets' / 'streamlit')

# *** utils

# ** util: streamlit_state
class StreamlitState(StateService):
    '''
    Adapts Streamlit's rerun-persistent session state to the MUI state
    contract, keeping host state access behind the dialect-specific edge.
    '''

    # * method: get
    def get(self, key: str) -> Any:
        '''
        Retrieve a value from the active Streamlit session.

        :param key: The session-state key.
        :type key: str
        :return: The stored session-state value.
        :rtype: Any
        '''

        # Read the current value through Streamlit's session-state mapping.
        return st.session_state[key]

    # * method: set
    def set(self, key: str, value: Any) -> None:
        '''
        Store a value in the active Streamlit session.

        :param key: The session-state key.
        :type key: str
        :param value: The value to persist for the session.
        :type value: Any
        :return: None
        :rtype: None
        '''

        # Persist the value through Streamlit's session-state mapping.
        st.session_state[key] = value
