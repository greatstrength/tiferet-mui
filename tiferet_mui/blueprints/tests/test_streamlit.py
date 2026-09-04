"""Streamlit binding blueprint tests."""

# *** imports

# ** app
from tiferet_mui.blueprints.streamlit import build_streamlit_binding
from tiferet_mui.domain import Element, Frame


# *** tests

# ** test: test_binding_mounts_component_and_dispatches_host_report
def test_binding_mounts_component_and_dispatches_host_report(monkeypatch):
    '''Test the binding renders the component and dispatches its on-change payload.'''

    # Capture declaration and component-call arguments without a Streamlit runtime.
    declaration = {}
    component_call = {}

    def component(**kwargs):
        '''Record component arguments and return the current report value.'''

        component_call.update(kwargs)
        return None

    def declare(name, path):
        '''Record declaration arguments and return the fake component instance.'''

        declaration.update({'name': name, 'path': path})
        return component

    # Supply a builder that records the dispatch closure and invokes it with a report.
    def handler_builder(key, dispatch):
        '''Build the fake Streamlit callback from the captured domain dispatcher.'''

        def on_change():
            '''Invoke dispatch with the confirmed component payload shape.'''
            return dispatch('{"callback_00": {}, "timestamp": 1788552865158}')

        return on_change

    # Replace the declaration boundary with the deterministic fake component.
    monkeypatch.setattr(
        'tiferet_mui.blueprints.streamlit.declare_component',
        declare,
    )
    handled = []
    frame = Frame(
        elements=[
            Element(
                type='Button',
                props={'onClick': lambda: handled.append('button clicked')},
            ),
        ],
    )

    # Build, mount, and trigger the plain binding callable.
    binding = build_streamlit_binding(handler_builder=handler_builder)
    binding(frame, key='mui_demo')
    component_call['on_change']()

    # Verify public declaration/render arguments and correct event delivery.
    assert declaration['name'] == 'muiElements'
    assert declaration['path'].endswith('tiferet_mui/assets/streamlit')
    assert component_call['key'] == 'mui_demo'
    assert 'render("muiElements","Button"' in component_call['js']
    assert handled == ['button clicked']
