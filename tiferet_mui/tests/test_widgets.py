"""Tiferet MUI widget catalog tests."""

# *** imports

# ** app
from tiferet_mui import box, button, text_field
from tiferet_mui.domain import Element

# *** tests

# ** test: test_button_describes_label_callback_and_props
def test_button_describes_label_callback_and_props():
    '''
    Test button creates the expected Element description.
    '''

    # Create a callback that can be compared by identity.
    def on_click():
        '''Provide a callback for the factory description.'''

    # Build a button with its common MUI properties.
    element = button(
        'Save',
        on_click=on_click,
        variant='contained',
    )

    # Verify the factory returns the expected Element tag and properties.
    assert isinstance(element, Element)
    assert element.type == 'Button'
    assert element.props == {
        'children': 'Save',
        'onClick': on_click,
        'variant': 'contained',
    }
    assert element.children == []


# ** test: test_text_field_describes_label_and_props
def test_text_field_describes_label_and_props():
    '''
    Test text_field creates the expected Element description.
    '''

    # Build a text field with its common MUI properties.
    element = text_field(
        'Name',
        fullWidth=True,
        variant='outlined',
    )

    # Verify the factory returns the expected Element tag and properties.
    assert isinstance(element, Element)
    assert element.type == 'TextField'
    assert element.props == {
        'label': 'Name',
        'fullWidth': True,
        'variant': 'outlined',
    }
    assert element.children == []


# ** test: test_box_describes_props_and_nested_elements
def test_box_describes_props_and_nested_elements():
    '''
    Test box creates the expected Element description with nested elements.
    '''

    # Compose a Box from other cataloged widget descriptions.
    element = box(
        text_field('Name'),
        button('Save'),
        sx={'padding': 2},
    )

    # Verify the factory preserves its tag, properties, and child elements.
    assert isinstance(element, Element)
    assert element.type == 'Box'
    assert element.props == {'sx': {'padding': 2}}
    assert [child.type for child in element.children] == ['TextField', 'Button']
