# AGENTS.md — Tiferet MUI (v1.0.0a5)

## Project Overview

**Tiferet MUI** is a small library for describing Material UI widget trees and
mounting them in Streamlit through Streamlit's public component API. A caller
composes a `Frame`, the package registers callbacks for its interactive
elements, and the Streamlit binding delivers reported interactions to those
callbacks.

- **Repository:** https://github.com/greatstrength/tiferet-mui
- **Prototype branch:** `v1.x-proto`
- **Python:** >= 3.10
- **Version:** `1.0.0a5`
- **Dependencies:** `tiferet >= 2.0.3`; optional `streamlit >= 1.36.0`

## Package Layout

```text
tiferet_mui/
├── __init__.py          — Package version
├── assets/              — Error data, widget defaults, DI registration data, and vendored Streamlit assets
├── blueprints/          — Host-agnostic handler composition and the Streamlit binding
├── di/                  — Code-declared StateService registration and DIContext factory
├── domain/              — Element, Frame, and CallbackTable domain objects
├── events/              — CreateElement, BuildCallbackTable, and DispatchCallback domain events
├── interfaces/          — StateService contract
├── mappers/             — CallbackTableAggregate and FrameTransferObject
├── utils/               — Streamlit session-state adapter and vendored bundle path helper
```

This package intentionally has no `contexts/` or `repos/` layer. The consuming
application owns its session and lifecycle; Tiferet MUI returns a binding
callable rather than owning a runtime hub.

## Key Concepts

- **Element** (`tiferet_mui/domain/element.py`) describes one widget using
  `type`, JSON-compatible `props`, and nested `children`.
- **Frame** (`tiferet_mui/domain/frame.py`) holds the root Elements for one
  render pass.
- **Widget defaults** (`tiferet_mui/assets/core.py`) define host-agnostic
  Button, TextField, and Box data shapes. They remain plain data and must not
  import domain or host layers.
- **CallbackTable** (`tiferet_mui/domain/callback_table.py`) is the immutable
  callback-id-to-handler registry built for a Frame.
- **CreateElement**, **BuildCallbackTable**, and **DispatchCallback**
  (`tiferet_mui/events/core.py`) respectively materialize an Element from a
  widget default, register interactive Elements, and route a reported callback
  to its handler.
- **Streamlit binding** (`tiferet_mui/blueprints/streamlit.py`) is the
  host-specific edge. It serializes a Frame for the vendored component and uses
  Streamlit's public `on_change` component callback.

Only the Streamlit-specific adapter modules and binding may import
`streamlit`. Domain models, events, mappers, interfaces, DI, and widget-default
data stay host-agnostic.

## Testing

- **Framework:** `pytest`
- **Test locations:** Co-located package tests, including
  `tiferet_mui/events/tests/test_events.py` for CreateElement coverage.
- **Full suite:** `pytest tiferet_mui/ -v`
- **Interactive demo E2E:** `pytest tiferet_mui/blueprints/tests/test_streamlit_e2e.py -v`
- **Manual demo:** `streamlit run examples/streamlit_binding_demo.py`

The Streamlit E2E test launches the example, clicks both vendored buttons via
Playwright, and verifies that each callback reaches the host application.

## Code Style

Follow Tiferet's structured artifact comments (`# ***`, `# **`, `# *`), RST
docstrings, and separated commented code snippets. Read the applicable
`tiferet-code-*` skill before changing a package layer.
