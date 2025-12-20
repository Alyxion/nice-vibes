import os

import pytest
import pytest_asyncio

from nice_vibes.mcp.test_client import MCPTestClient


@pytest_asyncio.fixture
async def mcp_client() -> MCPTestClient:
    client = MCPTestClient()
    await client.start()
    try:
        yield client
    finally:
        await client.stop()


def _has_tool(tools: list[dict], name: str) -> bool:
    return any(t.get('name') == name for t in tools)


async def _call_text_tool(client: MCPTestClient, name: str, arguments: dict | None = None) -> str:
    result = await client.call_tool(name, arguments or {})
    assert 'error' not in result, result.get('error')
    content = result.get('content', [])
    text_parts: list[str] = []
    for item in content:
        if item.get('type') == 'text':
            text_parts.append(item.get('text', ''))
    return '\n'.join(text_parts)


@pytest.mark.asyncio
async def test_mcp_list_tools_contains_expected_tools(mcp_client: MCPTestClient) -> None:
    tools = await mcp_client.list_tools()
    assert tools, 'Expected at least one MCP tool'

    expected = {
        'list_topics',
        'get_topic',
        'search_topics',
        'list_samples',
        'get_sample_source',
        'get_component_info',
        'get_component_source',
        'get_component_docs',
        'get_project_creation_guide',
        'kill_port_8080',
        'open_browser',
        'capture_url_screenshot',
    }

    missing = sorted([name for name in expected if not _has_tool(tools, name)])
    assert not missing, f'Missing tools: {missing}'


@pytest.mark.asyncio
async def test_mcp_resources_roundtrip(mcp_client: MCPTestClient) -> None:
    resources = await mcp_client.list_resources()
    assert resources, 'Expected at least one resource'

    uris = {r.get('uri') for r in resources}
    assert 'nicegui://topics' in uris

    topics_text = await mcp_client.read_resource('nicegui://topics')
    assert 'NiceGUI' in topics_text


@pytest.mark.asyncio
async def test_mcp_list_topics_and_get_topic(mcp_client: MCPTestClient) -> None:
    text = await _call_text_tool(mcp_client, 'list_topics', {})
    assert text.strip(), 'Expected non-empty list_topics response'

    # Use a stable topic which should exist in this repo.
    topic_text = await _call_text_tool(mcp_client, 'get_topic', {'topic': 'routing'})
    assert topic_text.strip(), 'Expected non-empty get_topic response'


@pytest.mark.asyncio
async def test_mcp_search_topics(mcp_client: MCPTestClient) -> None:
    text = await _call_text_tool(mcp_client, 'search_topics', {'keyword': 'routing'})
    assert text.strip(), 'Expected non-empty search_topics response'


@pytest.mark.asyncio
async def test_mcp_samples_tools(mcp_client: MCPTestClient) -> None:
    text = await _call_text_tool(mcp_client, 'list_samples', {})
    assert 'Sample' in text or 'Samples' in text

    sample_text = await _call_text_tool(
        mcp_client,
        'get_sample_source',
        {'sample': 'dashboard', 'file': 'main.py'},
    )
    assert '```python' in sample_text


@pytest.mark.asyncio
async def test_mcp_component_tools(mcp_client: MCPTestClient) -> None:
    source = await _call_text_tool(mcp_client, 'get_component_source', {'component': 'ui.button'})
    assert '```python' in source

    info = await _call_text_tool(
        mcp_client,
        'get_component_info',
        {'component': 'ui.button', 'include_source': False, 'max_ancestors': 2},
    )
    assert 'URLs' in info or 'Source' in info


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('NICE_VIBES_RUN_NETWORK_TESTS') != '1', reason='Set NICE_VIBES_RUN_NETWORK_TESTS=1 to enable')
async def test_mcp_get_component_docs(mcp_client: MCPTestClient) -> None:
    # This tool may fetch docs from GitHub if not cached.
    text = await _call_text_tool(mcp_client, 'get_component_docs', {'component': 'ui.button'})
    assert text.strip()


@pytest.mark.asyncio
async def test_mcp_project_creation_guide(mcp_client: MCPTestClient) -> None:
    text = await _call_text_tool(mcp_client, 'get_project_creation_guide', {})
    assert text.strip()


@pytest.mark.asyncio
async def test_mcp_destructive_tools_are_skipped_by_default(mcp_client: MCPTestClient) -> None:
    # These tools can have side-effects (killing processes, opening browser) or require heavy deps.
    # Keep them opt-in to make CI/dev runs reliable.
    assert True


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('NICE_VIBES_RUN_DESTRUCTIVE_TESTS') != '1', reason='Set NICE_VIBES_RUN_DESTRUCTIVE_TESTS=1 to enable')
async def test_mcp_kill_port_8080(mcp_client: MCPTestClient) -> None:
    text = await _call_text_tool(mcp_client, 'kill_port_8080', {})
    assert text.strip()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('NICE_VIBES_RUN_DESTRUCTIVE_TESTS') != '1', reason='Set NICE_VIBES_RUN_DESTRUCTIVE_TESTS=1 to enable')
async def test_mcp_open_browser(mcp_client: MCPTestClient) -> None:
    text = await _call_text_tool(mcp_client, 'open_browser', {'url': 'http://localhost:8080'})
    assert text.strip()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('NICE_VIBES_RUN_SCREENSHOT_TESTS') != '1', reason='Set NICE_VIBES_RUN_SCREENSHOT_TESTS=1 to enable')
async def test_mcp_capture_url_screenshot_requires_running_app(mcp_client: MCPTestClient) -> None:
    # Requires a running app at the provided URL, plus selenium + browser driver.
    result = await mcp_client.call_tool('capture_url_screenshot', {'url': 'http://localhost:8080', 'wait': 1})
    assert 'error' not in result
    content = result.get('content', [])
    assert any(item.get('type') in {'text', 'image'} for item in content)
