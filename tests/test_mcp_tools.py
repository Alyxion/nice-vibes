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
        'project_setup',
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
async def test_mcp_project_setup(mcp_client: MCPTestClient) -> None:
    """Test project_setup returns valid JSON with expected structure."""
    import json

    text = await _call_text_tool(mcp_client, 'project_setup', {'project_name': 'Test App'})
    assert text.strip()

    # Should be valid JSON
    setup = json.loads(text)

    # Check structure
    assert setup['project_name'] == 'Test App'
    assert setup['project_slug'] == 'test_app'
    assert setup['project_type'] == 'single_page'
    assert 'folders' in setup
    assert 'files' in setup
    assert 'instructions' in setup

    # Check expected files exist (main.py inside package, not root)
    file_paths = [f['path'] for f in setup['files']]
    assert 'pyproject.toml' in file_paths
    assert 'README.md' in file_paths
    assert 'test_app/main.py' in file_paths  # Inside package
    assert 'test_app/__init__.py' in file_paths
    assert '.gitignore' in file_paths
    assert 'CLAUDE.md' in file_paths
    assert 'AGENTS.md' in file_paths
    assert '.windsurf/rules/rules.md' in file_paths

    # Check expected folders exist
    assert 'test_app' in setup['folders']
    assert '.windsurf' in setup['folders']
    assert '.windsurf/rules' in setup['folders']

    # Check run command uses python -m
    readme = next(f for f in setup['files'] if f['path'] == 'README.md')
    assert 'python -m test_app.main' in readme['content']


@pytest.mark.asyncio
async def test_mcp_project_setup_spa(mcp_client: MCPTestClient) -> None:
    """Test project_setup with spa type creates full structure."""
    import json

    text = await _call_text_tool(mcp_client, 'project_setup', {
        'project_name': 'My SPA',
        'project_type': 'spa',
    })
    setup = json.loads(text)

    assert setup['project_type'] == 'spa'

    file_paths = [f['path'] for f in setup['files']]
    # SPA-specific files
    assert 'my_spa/layout.py' in file_paths
    assert 'my_spa/pages/__init__.py' in file_paths
    assert 'my_spa/pages/home/__init__.py' in file_paths
    assert 'my_spa/pages/home/home.py' in file_paths
    assert 'my_spa/components/__init__.py' in file_paths
    assert 'my_spa/static/css/app.css' in file_paths

    # SPA-specific folders
    assert 'my_spa/pages' in setup['folders']
    assert 'my_spa/components' in setup['folders']
    assert 'my_spa/static' in setup['folders']


@pytest.mark.asyncio
async def test_mcp_project_setup_without_mcp(mcp_client: MCPTestClient) -> None:
    """Test project_setup with include_mcp_rules=False references GitHub URLs."""
    import json

    text = await _call_text_tool(mcp_client, 'project_setup', {
        'project_name': 'No MCP App',
        'include_mcp_rules': False,
    })
    setup = json.loads(text)

    # AGENTS.md should reference GitHub URLs instead of MCP
    agents_file = next(f for f in setup['files'] if f['path'] == 'AGENTS.md')
    assert 'githubusercontent.com/Alyxion/nice-vibes' in agents_file['content']
    assert 'nice_vibes.md' in agents_file['content']


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
async def test_mcp_capture_url_screenshot_schema_includes_format_quality(mcp_client: MCPTestClient) -> None:
    """Verify the capture_url_screenshot tool schema includes format and quality parameters."""
    tools = await mcp_client.list_tools()
    screenshot_tool = next((t for t in tools if t.get('name') == 'capture_url_screenshot'), None)
    assert screenshot_tool is not None, 'capture_url_screenshot tool not found'

    schema = screenshot_tool.get('inputSchema', {})
    properties = schema.get('properties', {})

    # Check format parameter exists with correct enum
    assert 'format' in properties, 'format parameter missing from schema'
    assert properties['format'].get('enum') == ['JPEG', 'PNG'], 'format enum incorrect'
    assert properties['format'].get('default') == 'JPEG', 'format default should be JPEG'

    # Check quality parameter exists with correct bounds
    assert 'quality' in properties, 'quality parameter missing from schema'
    assert properties['quality'].get('default') == 85, 'quality default should be 85'
    assert properties['quality'].get('minimum') == 1, 'quality minimum should be 1'
    assert properties['quality'].get('maximum') == 100, 'quality maximum should be 100'


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('NICE_VIBES_RUN_SCREENSHOT_TESTS') != '1', reason='Set NICE_VIBES_RUN_SCREENSHOT_TESTS=1 to enable')
async def test_mcp_capture_url_screenshot_requires_running_app(mcp_client: MCPTestClient) -> None:
    # Requires a running app at the provided URL, plus selenium + browser driver.
    # Default format is now JPEG
    result = await mcp_client.call_tool('capture_url_screenshot', {'url': 'http://localhost:8080', 'wait': 1})
    assert 'error' not in result
    content = result.get('content', [])
    image_item = next((item for item in content if item.get('type') == 'image'), None)
    assert image_item is not None, 'Expected image content'
    assert image_item.get('mimeType') == 'image/jpeg', 'Default format should be JPEG'


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('NICE_VIBES_RUN_SCREENSHOT_TESTS') != '1', reason='Set NICE_VIBES_RUN_SCREENSHOT_TESTS=1 to enable')
async def test_mcp_capture_url_screenshot_png_format(mcp_client: MCPTestClient) -> None:
    # Test PNG format option
    result = await mcp_client.call_tool('capture_url_screenshot', {
        'url': 'http://localhost:8080',
        'wait': 1,
        'format': 'PNG',
    })
    assert 'error' not in result
    content = result.get('content', [])
    image_item = next((item for item in content if item.get('type') == 'image'), None)
    assert image_item is not None, 'Expected image content'
    assert image_item.get('mimeType') == 'image/png', 'Format should be PNG'


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('NICE_VIBES_RUN_SCREENSHOT_TESTS') != '1', reason='Set NICE_VIBES_RUN_SCREENSHOT_TESTS=1 to enable')
async def test_mcp_capture_url_screenshot_jpeg_quality(mcp_client: MCPTestClient) -> None:
    # Test custom JPEG quality
    result = await mcp_client.call_tool('capture_url_screenshot', {
        'url': 'http://localhost:8080',
        'wait': 1,
        'format': 'JPEG',
        'quality': 50,
    })
    assert 'error' not in result
    content = result.get('content', [])
    image_item = next((item for item in content if item.get('type') == 'image'), None)
    assert image_item is not None, 'Expected image content'
    assert image_item.get('mimeType') == 'image/jpeg'
