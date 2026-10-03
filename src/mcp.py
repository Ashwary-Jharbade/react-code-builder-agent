# src/mcp.py
from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_client = MultiServerMCPClient(
    {
        "chrome": {
            "transport": "stdio",
            "command": "npx",
            "args": [
                "-y",
                "chrome-devtools-mcp@latest",
                "--no-usage-statistics",
                "--no-performance-crux"
            ],
        }
    }
)

async def get_tools():
    tools = await mcp_client.get_tools()
    for tool in tools:
        print(tool.name)
    return tools