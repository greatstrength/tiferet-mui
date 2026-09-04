"""Run with: streamlit run examples/streamlit_binding_demo.py."""

# *** imports

# ** infra
import streamlit as st

# ** app
from tiferet_mui.blueprints.streamlit import build_streamlit_binding
from tiferet_mui.domain import Element, Frame

# *** functions

# ** function: record_button
def record_button() -> None:
    '''Record a button interaction in the host-owned Streamlit session.

    :return: None
    :rtype: None
    '''

    # Record which registered callback handled the latest host report.
    st.session_state['mui_demo_result'] = 'Button callback delivered.'


# ** function: record_second_button
def record_second_button() -> None:
    '''Record a second button interaction in the host-owned Streamlit session.

    :return: None
    :rtype: None
    '''

    # Record that the second callback table entry received its host report.
    st.session_state['mui_demo_result'] = 'Second button callback delivered.'


# *** blueprints

# ** blueprint: render_demo
def render_demo() -> None:
    '''Render two interactive vendored elements through the Streamlit Binding.

    :return: None
    :rtype: None
    '''

    # Compose a fresh frame with two handlers for this Streamlit rerun.
    frame = Frame(
        elements=[
            Element(
                type='Button',
                props={
                    'children': 'Trigger callback',
                    'onClick': record_button,
                },
            ),
            Element(
                type='Button',
                props={
                    'children': 'Trigger second callback',
                    'onClick': record_second_button,
                },
            ),
        ],
    )

    # Build the plain binding and mount this frame with a stable widget key.
    binding = build_streamlit_binding()
    binding(frame, key='tiferet_mui_demo')

    # Display the last callback outcome owned by the host application session.
    st.write(st.session_state.get('mui_demo_result', 'Awaiting interaction.'))


# Render the standalone Streamlit demo.
render_demo()
