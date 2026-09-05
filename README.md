# tiferet-mui

Tiferet MUI lets a Streamlit application describe and render Material UI
widgets through Streamlit's supported public component API. It keeps widget
trees and callback routing host-agnostic, while the optional Streamlit binding
handles mounting and interaction delivery.

## Install

Install the core package when you only need its domain models and widget
catalog:

```bash
pip install tiferet-mui
```

Install the Streamlit extra to render a `Frame` in a Streamlit application:

```bash
pip install "tiferet-mui[streamlit]"
```

## Minimal usage

Compose a `Frame` from the widget catalog, then mount it with the Streamlit
binding:

```python
from tiferet_mui import box, button, text_field
from tiferet_mui.blueprints.streamlit import build_streamlit_binding
from tiferet_mui.domain import Frame


def save() -> None:
    print('Saved.')


frame = Frame(
    elements=[
        box(
            text_field('Name', fullWidth=True),
            button('Save', on_click=save, variant='contained'),
            sx={'display': 'grid', 'gap': 2},
        ),
    ],
)

build_streamlit_binding()(frame, key='profile_form')
```

Run the included interactive example with:

```bash
streamlit run examples/streamlit_binding_demo.py
```
