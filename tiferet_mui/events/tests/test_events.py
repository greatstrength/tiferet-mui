"""Tiferet MUI Callback Event Tests."""

# *** imports

# ** infra
import pytest

# ** app
from tiferet.assets import TiferetError
from tiferet.testing import DomainEventTestBase

from tiferet_mui.assets import (
    CALLBACK_NOT_FOUND_ID,
    WIDGET_TYPE_NOT_FOUND_ID,
)
from tiferet_mui.domain import CallbackTable, Frame
from tiferet_mui.events import (
    BuildCallbackTable,
    CreateElement,
    DispatchCallback,
)
from tiferet_mui.mappers import CallbackTableAggregate

# *** functions

# ** function: button_handler
def button_handler(**kwargs):
    '''
    Return the parameters reported by a button interaction.

    :param kwargs: The callback parameters.
    :type kwargs: dict
    :return: The supplied callback parameters.
    :rtype: dict
    '''

    # Return the supplied callback parameters.
    return kwargs

# ** function: text_handler
def text_handler(**kwargs):
    '''
    Return the parameters reported by a text interaction.

    :param kwargs: The callback parameters.
    :type kwargs: dict
    :return: The supplied callback parameters.
    :rtype: dict
    '''

    # Return the supplied callback parameters.
    return kwargs

# *** constants

# ** constant: frame
FRAME = Frame(
    elements=[
        {
            'type': 'Stack',
            'children': [
                {
                    'type': 'Button',
                    'props': {'onClick': button_handler},
                },
                {
                    'type': 'TextField',
                    'props': {'onChange': text_handler},
                },
            ],
        },
    ],
)

# ** constant: callback_table
CALLBACK_TABLE = CallbackTable(
    handlers={'button_00': button_handler},
)

# *** tests

# ** test: TestCreateElement
class TestCreateElement(DomainEventTestBase):
    '''
    Tests Element construction through the DomainEvent test harness.
    '''

    # * attribute: event_cls
    event_cls = CreateElement

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {'widget_type': 'button'}

    # * attribute: required_params
    required_params = ['widget_type']

    # * method: test_merges_widget_defaults_props_and_children
    def test_merges_widget_defaults_props_and_children(self, mock_dependencies):
        '''
        Test the event combines defaults, MUI properties, and nested elements.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Create a Button with property overrides and one nested Element child.
        element = self.handle(
            mock_dependencies,
            props={
                'children': 'Save',
                'color': 'primary',
                'variant': 'outlined',
            },
            children=[
                {
                    'type': 'TextField',
                    'props': {'label': 'Name'},
                },
            ],
        )

        # Verify props override defaults without replacing Element children.
        assert element.type == 'Button'
        assert element.props == {
            'children': 'Save',
            'color': 'primary',
            'variant': 'outlined',
        }
        assert len(element.children) == 1
        assert element.children[0].type == 'TextField'
        assert element.children[0].props == {'label': 'Name'}

    # * method: test_raises_for_unrecognized_widget_type
    def test_raises_for_unrecognized_widget_type(self, mock_dependencies):
        '''
        Test an unknown widget type raises the catalogued domain error.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Request a widget type without any registered default shape.
        with pytest.raises(TiferetError) as error:
            self.handle(
                mock_dependencies,
                widget_type='unknown',
            )

        # Verify the event surfaces the catalogue lookup error.
        assert error.value.error_code == WIDGET_TYPE_NOT_FOUND_ID

# ** test: TestBuildCallbackTable
class TestBuildCallbackTable(DomainEventTestBase):
    '''
    Tests callback-table construction through the DomainEvent test harness.
    '''

    # * attribute: event_cls
    event_cls = BuildCallbackTable

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {'frame': FRAME}

    # * attribute: required_params
    required_params = ['frame']

    # * method: test_builds_frozen_table_with_distinct_callback_ids
    def test_builds_frozen_table_with_distinct_callback_ids(self, mock_dependencies):
        '''
        Test a tree walk registers multiple handlers under distinct identifiers.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Build the callback table through DomainEvent.handle.
        callback_table = self.handle(mock_dependencies)

        # Verify every interactive element received a unique identifier.
        button, text = FRAME.elements[0].children
        assert button.props['callback_id'] != text.props['callback_id']
        assert callback_table.handlers == {
            button.props['callback_id']: button_handler,
            text.props['callback_id']: text_handler,
        }

        # Verify callers receive the frozen domain object, not the aggregate.
        assert isinstance(callback_table, CallbackTable)
        assert not isinstance(callback_table, CallbackTableAggregate)
        with pytest.raises(AttributeError):
            callback_table.register('unexpected', button_handler)

# ** test: TestDispatchCallback
class TestDispatchCallback(DomainEventTestBase):
    '''
    Tests callback dispatch through the DomainEvent test harness.
    '''

    # * attribute: event_cls
    event_cls = DispatchCallback

    # * attribute: dependencies
    dependencies = {}

    # * attribute: sample_kwargs
    sample_kwargs = {
        'callback_table': CALLBACK_TABLE,
        'payload': {
            'button_00': {'value': 'clicked'},
            'timestamp': 1788552865158,
        },
    }

    # * attribute: required_params
    required_params = ['callback_table', 'payload']

    # * method: test_dispatches_registered_callback
    def test_dispatches_registered_callback(self, mock_dependencies):
        '''
        Test the registered handler receives its payload-defined parameters.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Dispatch the confirmed composite payload through DomainEvent.handle.
        result = self.handle(mock_dependencies)

        # Verify the matching handler returned its interaction parameters.
        assert result == {'value': 'clicked'}

    # * method: test_raises_for_unrecognized_callback_id
    def test_raises_for_unrecognized_callback_id(self, mock_dependencies):
        '''
        Test an interaction without a registered handler is a domain error.

        :param mock_dependencies: The harness-provided event dependencies.
        :type mock_dependencies: dict
        '''

        # Dispatch an interaction whose callback ID was not registered.
        with pytest.raises(TiferetError) as error:
            self.handle(
                mock_dependencies,
                payload={
                    'unknown_00': {},
                    'timestamp': 1788552865158,
                },
            )

        # Verify dispatch reports the catalogued callback-not-found outcome.
        assert error.value.error_code == CALLBACK_NOT_FOUND_ID
