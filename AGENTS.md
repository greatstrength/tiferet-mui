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
├── blueprints/          — build_frame composition, host callbacks, and the Streamlit binding
├── di/                  — Code-declared StateService registration and DIContext factory
├── domain/              — Element, Frame, and CallbackTable domain objects
├── events/              — CreateElement, CreateFrame, BuildCallbackTable, and DispatchCallback events
├── interfaces/          — StateService contract
├── mappers/             — Element/Frame/CallbackTable aggregates and FrameTransferObject
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
- **ElementAggregate** and **FrameAggregate** (`tiferet_mui/mappers/`) provide
  validated mutation surfaces, then freeze the Element and Frame snapshots
  returned to callers.
- **Widget defaults** (`tiferet_mui/assets/core.py`) define host-agnostic
  Button, TextField, and Box data shapes. They remain plain data and must not
  import domain or host layers.
- **CallbackTable** (`tiferet_mui/domain/callback_table.py`) is the immutable
  callback-id-to-handler registry built for a Frame.
- **CreateElement**, **CreateFrame**, **BuildCallbackTable**, and
  **DispatchCallback** (`tiferet_mui/events/core.py`) respectively materialize
  an Element from defaults, recursively assemble a Frame, register interactive
  Elements, and route a reported callback to its handler.
- **build_frame** (`tiferet_mui/blueprints/core.py`) is the consumer-facing
  composition entrypoint: it accepts recursive widget specs and returns a
  ready-to-mount Frame without exposing the domain/event construction layers.
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
