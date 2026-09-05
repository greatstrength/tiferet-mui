"""Live Streamlit browser test for the vendored MUI binding."""

# *** imports

# ** core
import socket
import subprocess
import sys
from pathlib import Path
from time import sleep
from urllib.request import urlopen

# ** infra
import pytest

# *** functions

# ** function: _find_open_port
def _find_open_port() -> int:
    '''
    Return an available loopback TCP port for one temporary test server.

    :return: An available loopback TCP port.
    :rtype: int
    '''

    # Let the operating system allocate an available loopback port.
    with socket.socket() as server:
        server.bind(('127.0.0.1', 0))
        return server.getsockname()[1]

# ** function: _wait_for_server
def _wait_for_server(url: str) -> None:
    '''
    Wait until the temporary Streamlit server accepts HTTP requests.

    :param url: The server URL whose health endpoint is polled.
    :type url: str
    :return: None
    :rtype: None
    '''

    # Poll briefly because Streamlit initializes asynchronously.
    for _ in range(50):
        try:
            with urlopen(url, timeout=1):
                return
        except OSError:
            sleep(.1)

    # Fail with an ordinary assertion when the server does not become healthy.
    pytest.fail(f'Streamlit server did not start at {url}.')

# *** tests

# ** test: test_demo_dispatches_each_real_button_interaction
def test_demo_dispatches_each_real_button_interaction():
    '''
    Test two browser clicks reach their distinct handlers through Streamlit.
    '''

    # Skip cleanly for contributors who have not installed browser test tooling.
    playwright = pytest.importorskip('playwright.sync_api')
    pytest.importorskip('streamlit')
    port = _find_open_port()
    repository_root = Path(__file__).parents[3]
    demo_path = repository_root / 'examples' / 'streamlit_binding_demo.py'
    url = f'http://127.0.0.1:{port}'
    process = subprocess.Popen(
        [
            sys.executable,
            '-m',
            'streamlit',
            'run',
            str(demo_path),
            '--server.headless',
            'true',
            '--server.port',
            str(port),
            '--browser.gatherUsageStats',
            'false',
        ],
        cwd=repository_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Wait for the temporary app before connecting a real headless browser.
        _wait_for_server(url + '/_stcore/health')

        # Click each vendored MUI button and verify its distinct host-side result.
        with playwright.sync_playwright() as browser_api:
            browser = browser_api.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            frame = page.frame_locator('iframe')
            frame.get_by_role('button', name='TRIGGER CALLBACK').click()
            page.get_by_text('Button callback delivered.').wait_for()
            frame = page.frame_locator('iframe')
            frame.get_by_role('button', name='TRIGGER SECOND CALLBACK').click()
            page.get_by_text('Second button callback delivered.').wait_for()
            browser.close()
    finally:
        # Stop the temporary Streamlit process even when browser assertions fail.
        process.terminate()
        process.wait(timeout=10)
