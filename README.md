# tiferet-mui

Tiferet MUI lets a Streamlit application describe and render Material UI
widgets through Streamlit's supported public component API. It keeps widget
trees and callback routing host-agnostic, while the optional Streamlit binding
handles mounting and interaction delivery.

## Install

Install the core package when you only need its domain models, widget defaults,
and domain events:

```bash
pip install tiferet-mui
```

Install the Streamlit extra to render a `Frame` in a Streamlit application:

```bash
pip install "tiferet-mui[streamlit]"
```

## Minimal usage

Materialize `Element` instances from the catalogued widget defaults, compose a
`Frame`, then mount it with the Streamlit binding:

```python
from tiferet.events import DomainEvent
from tiferet_mui.blueprints.streamlit import build_streamlit_binding
from tiferet_mui.domain import Frame
from tiferet_mui.events import CreateElement


def save() -> None:
    print('Saved.')


frame = Frame(
    elements=[
        DomainEvent.handle(
            CreateElement,
            widget_type='box',
            props={'sx': {'display': 'grid', 'gap': 2}},
            children=[
                DomainEvent.handle(
                    CreateElement,
                    widget_type='text_field',
                    props={'label': 'Name', 'fullWidth': True},
                ),
                DomainEvent.handle(
                    CreateElement,
                    widget_type='button',
                    props={'children': 'Save', 'onClick': save},
                ),
            ],
        ),
    ],
)

build_streamlit_binding()(frame, key='profile_form')
```

Run the included interactive example with:

```bash
streamlit run examples/streamlit_binding_demo.py
```
