"""Host-agnostic Material UI Element factories."""

# *** imports

# ** core
from typing import Any, Callable

# ** app
from .domain import Element

# *** functions

# ** function: button
def button(
        label: str,
        on_click: Callable[[], Any] | None = None,
        **props: Any,
    ) -> Element:
    '''
    Create a Material UI Button description with an optional click handler.

    :param label: The text rendered inside the button.
    :type label: str
    :param on_click: Optional handler invoked when the button is clicked.
    :type on_click: Callable[[], Any] | None
    :param props: Additional Material UI Button properties.
    :type props: Any
    :return: The described Button element.
    :rtype: Element
    '''

    # Start with the MUI Button label and preserve caller-supplied properties.
    button_props = {
        'children': label,
        **props,
    }

    # Translate the Python callback argument into the MUI click property.
    if on_click is not None:
        button_props['onClick'] = on_click

    # Return the host-agnostic Button description.
    return Element(type='Button', props=button_props)


# ** function: text_field
def text_field(label: str, **props: Any) -> Element:
    '''
    Create a Material UI TextField description.

    :param label: The label displayed for the text field.
    :type label: str
    :param props: Additional Material UI TextField properties.
    :type props: Any
    :return: The described TextField element.
    :rtype: Element
    '''

    # Start with the MUI TextField label and preserve caller-supplied properties.
    text_field_props = {
        'label': label,
        **props,
    }

    # Return the host-agnostic TextField description.
    return Element(type='TextField', props=text_field_props)


# ** function: box
def box(*children: Element, **props: Any) -> Element:
    '''
    Create a Material UI Box description that contains child elements.

    :param children: The elements nested in the box.
    :type children: Element
    :param props: Additional Material UI Box properties.
    :type props: Any
    :return: The described Box element.
    :rtype: Element
    '''

    # Materialize the supplied children for Element's JSON-compatible tree shape.
    element_children = list(children)

    # Return the host-agnostic Box description.
    return Element(
        type='Box',
        props=props,
        children=element_children,
    )
