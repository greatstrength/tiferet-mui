"""Streamlit utility tests."""

# *** imports

# ** core
from pathlib import Path

# ** infra
import streamlit as st

# ** app
from tiferet_mui.interfaces import StateService
from tiferet_mui.utils.streamlit import StreamlitState, get_streamlit_bundle_path

# *** tests

# ** test: test_streamlit_state_proxies_session_state
def test_streamlit_state_proxies_session_state(monkeypatch):
    '''Test StreamlitState reads and writes the current Streamlit state mapping.'''

    # Replace Streamlit's runtime state proxy with a deterministic mapping.
    session_state = {}
    monkeypatch.setattr(st, 'session_state', session_state)
    state_service = StreamlitState()

    # Store and retrieve a value through the StateService contract.
    state_service.set('component', {'callback_00': {}})

    # Verify the adapter remains a StateService and proxies its backing mapping.
    assert isinstance(state_service, StateService)
    assert state_service.get('component') == {'callback_00': {}}
    assert session_state['component'] == {'callback_00': {}}


# ** test: test_bundle_path_resolves_vendored_component
def test_bundle_path_resolves_vendored_component():
    '''Test the component path resolves to the packaged frontend entrypoint.'''

    # Resolve the filesystem path supplied to declare_component.
    bundle_path = get_streamlit_bundle_path()

    # Verify the vendored frontend entrypoint exists at that path.
    assert bundle_path.endswith('tiferet_mui/assets/streamlit')
    assert (Path(bundle_path) / 'index.html').is_file()
