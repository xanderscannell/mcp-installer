"""Minimal MCP server — no dependencies required.
See the full spec at https://modelcontextprotocol.io
"""

import json
import sys

SERVER_NAME = "YOUR_PLUGIN_NAME"
SERVER_VERSION = "1.0.0"

# --- Define your tools here ---

async def hello_handler(params):
    return {
        "content": [{"type": "text", "text": "Hello from your MCP plugin!"}]
    }

tools = {
    "hello": {
        "description": "A simple greeting tool",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": hello_handler,
    },
}

# --- Define your resources here ---

# async def example_handler(uri):
#     return {
#         "contents": [{"uri": uri, "text": "Example resource data"}]
#     }
#
# resources = {
#     "example://data": {
#         "name": "Example",
#         "description": "An example resource",
#         "mimeType": "text/plain",
#         "handler": example_handler,
#     },
# }

resources = {}

# --- MCP Protocol (JSON-RPC over stdio) ---

import asyncio

async def handle_request(method, params):
    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {} if tools else None,
                "resources": {} if resources else None,
            },
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        }

    elif method == "tools/list":
        return {
            "tools": [
                {
                    "name": name,
                    "description": t["description"],
                    "inputSchema": t["inputSchema"],
                }
                for name, t in tools.items()
            ]
        }

    elif method == "tools/call":
        tool = tools.get(params.get("name"))
        if not tool:
            raise JsonRpcError(-32602, f"Unknown tool: {params.get('name')}")
        return await tool["handler"](params.get("arguments", {}))

    elif method == "resources/list":
        return {
            "resources": [
                {
                    "uri": uri,
                    "name": r["name"],
                    "description": r["description"],
                    "mimeType": r["mimeType"],
                }
                for uri, r in resources.items()
            ]
        }

    elif method == "resources/read":
        resource = resources.get(params.get("uri"))
        if not resource:
            raise JsonRpcError(-32602, f"Unknown resource: {params.get('uri')}")
        return await resource["handler"](params["uri"])

    elif method == "ping":
        return {}

    else:
        raise JsonRpcError(-32601, f"Method not found: {method}")


class JsonRpcError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


def send(message):
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


async def main():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    buffer = b""
    while True:
        chunk = await reader.read(4096)
        if not chunk:
            break
        buffer += chunk
        *lines, buffer = buffer.split(b"\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
                continue

            # Notifications (no id) — nothing to respond to
            if "id" not in msg:
                continue

            try:
                result = await handle_request(msg.get("method"), msg.get("params", {}))
                send({"jsonrpc": "2.0", "id": msg["id"], "result": result})
            except JsonRpcError as err:
                send({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": err.code, "message": err.message}})
            except Exception as err:
                send({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32603, "message": str(err)}})


if __name__ == "__main__":
    asyncio.run(main())
