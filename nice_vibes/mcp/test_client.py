#!/usr/bin/env python3
"""
Interactive test client for the NiceGUI MCP server.

This client communicates with the MCP server via JSON-RPC over stdio,
allowing you to test all server functionality interactively.

Usage:
    poetry run python -m nice_vibes.mcp.test_client
"""

import asyncio
import json
import shutil
import sys
import textwrap
from pathlib import Path


class MCPTestClient:
    """Test client for MCP server via subprocess."""
    
    def __init__(self):
        self.process = None
        self.request_id = 0
        self._read_task = None
        self._pending_responses = {}
    
    async def start(self):
        """Start the MCP server subprocess."""
        python = sys.executable
        server_module = "nice_vibes.mcp"
        cwd = Path(__file__).parent.parent.parent
        
        self.process = await asyncio.create_subprocess_exec(
            python, "-m", server_module,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )
        
        # Start reading stderr in background (for server logs)
        self._stderr_task = asyncio.create_task(self._read_stderr())
        
        print("Server started. Initializing...")
        
        # Initialize the connection
        await self._initialize()
    
    async def _read_stderr(self):
        """Read and print stderr from server."""
        while True:
            line = await self.process.stderr.readline()
            if not line:
                break
            print(f"[SERVER] {line.decode().strip()}", file=sys.stderr)
    
    async def _send_request(self, method: str, params: dict = None) -> dict:
        """Send a JSON-RPC request and wait for response."""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
        }
        if params:
            request["params"] = params
        
        # Send request
        request_json = json.dumps(request)
        self.process.stdin.write(request_json.encode() + b"\n")
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("Server closed connection")
        
        response = json.loads(response_line.decode())
        return response
    
    async def _initialize(self):
        """Initialize the MCP connection."""
        response = await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        
        if "error" in response:
            print(f"Initialize error: {response['error']}")
            return
        
        print(f"Server: {response.get('result', {}).get('serverInfo', {})}")
        
        # Send initialized notification
        notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        self.process.stdin.write(json.dumps(notification).encode() + b"\n")
        await self.process.stdin.drain()
    
    async def list_tools(self) -> list:
        """List available tools."""
        response = await self._send_request("tools/list")
        if "error" in response:
            print(f"Error: {response['error']}")
            return []
        return response.get("result", {}).get("tools", [])
    
    async def call_tool(self, name: str, arguments: dict = None) -> dict:
        """Call a tool."""
        params = {"name": name}
        if arguments:
            params["arguments"] = arguments
        
        response = await self._send_request("tools/call", params)
        if "error" in response:
            return {"error": response["error"]}
        return response.get("result", {})
    
    async def list_resources(self) -> list:
        """List available resources."""
        response = await self._send_request("resources/list")
        if "error" in response:
            print(f"Error: {response['error']}")
            return []
        return response.get("result", {}).get("resources", [])
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource."""
        response = await self._send_request("resources/read", {"uri": uri})
        if "error" in response:
            return f"Error: {response['error']}"
        contents = response.get("result", {}).get("contents", [])
        if contents:
            return contents[0].get("text", "")
        return ""
    
    async def stop(self):
        """Stop the server."""
        if self.process:
            self.process.terminate()
            await self.process.wait()


async def interactive_session():
    """Run an interactive test session."""
    client = MCPTestClient()
    
    try:
        await client.start()
        
        print("\n" + "="*60)
        print("Nice Vibes MCP Server Test Client")
        print("="*60)
        print("\nCommands:")
        print("  tools          - List available tools")
        print("  resources      - List available resources")
        print("  call <tool>    - Call a tool (will prompt for args)")
        print("  read <uri>     - Read a resource")
        print("  quit           - Exit")
        print()
        
        while True:
            try:
                cmd = input("\n> ").strip()
            except EOFError:
                break
            
            if not cmd:
                continue
            
            parts = cmd.split(maxsplit=1)
            command = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""
            
            if command == "quit" or command == "exit":
                break
            
            elif command == "tools":
                tools = await client.list_tools()
                print(f"\nAvailable tools ({len(tools)}):")
                for tool in tools:
                    name = tool.get('name', '')
                    desc = (tool.get('description', '') or '').replace('\n', ' ')
                    print(f"  - {name}: {desc}")
            
            elif command == "resources":
                resources = await client.list_resources()
                print(f"\nAvailable resources ({len(resources)}):")
                for res in resources:
                    print(f"  - {res['uri']}: {res.get('name', '')}")
            
            elif command == "call":
                if not arg:
                    print("Usage: call <tool_name>")
                    continue
                
                tool_name = arg
                
                # Get tool info
                tools = await client.list_tools()
                tool = next((t for t in tools if t['name'] == tool_name), None)
                
                if not tool:
                    print(f"Unknown tool: {tool_name}")
                    continue
                
                # Build arguments
                schema = tool.get('inputSchema', {})
                properties = schema.get('properties', {})
                required = schema.get('required', [])
                
                arguments = {}
                for prop_name, prop_info in properties.items():
                    is_required = prop_name in required
                    prompt = f"  {prop_name}"
                    if prop_info.get('description'):
                        prompt += f" ({prop_info['description']})"
                    if not is_required:
                        prompt += " [optional]"
                    prompt += ": "
                    
                    value = input(prompt).strip()
                    if value:
                        # Try to parse as JSON for complex types
                        try:
                            arguments[prop_name] = json.loads(value)
                        except json.JSONDecodeError:
                            arguments[prop_name] = value
                    elif is_required:
                        print(f"  {prop_name} is required!")
                        break
                else:
                    # All args collected, call the tool
                    print(f"\nCalling {tool_name}...")
                    result = await client.call_tool(tool_name, arguments)
                    
                    if "error" in result:
                        print(f"Error: {result['error']}")
                    else:
                        content = result.get('content', [])
                        for item in content:
                            if item.get('type') == 'text':
                                text = item.get('text', '')
                                print(text)
                            elif item.get('type') == 'image':
                                print(f"[Image: {item.get('mimeType', 'unknown')} - {len(item.get('data', ''))} bytes base64]")
            
            elif command == "read":
                if not arg:
                    print("Usage: read <uri>")
                    continue
                
                content = await client.read_resource(arg)
                print(content)
            
            else:
                print(f"Unknown command: {command}")
    
    finally:
        await client.stop()
        print("\nGoodbye!")


def main():
    """Entry point."""
    asyncio.run(interactive_session())


if __name__ == "__main__":
    main()
