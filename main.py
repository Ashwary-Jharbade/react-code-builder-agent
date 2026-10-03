
from dotenv import load_dotenv
import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from deepagents.backends import FilesystemBackend
from deepagents import create_deep_agent
from deepagents.middleware import FilesystemMiddleware
from models import model

load_dotenv()
CONTEXT7_API_KEY = os.getenv("CONTEXT7_API_KEY")

backend = FilesystemBackend(
    root_dir="./aidrivenproject",
    virtual_mode=True,
)

mcp_client = MultiServerMCPClient(
    {
        # "context7": {
        #     "transport": "http",
        #     "url": "https://mcp.context7.com/mcp",
        #     "headers": {
        #         "Authorization": f"Bearer {CONTEXT7_API_KEY}",
        #     },
        # },
        # "filesystem": {
        #     "transport": "stdio",
        #     "command": "npx",
        #     "args": [
        #         "-y",
        #         "@modelcontextprotocol/server-filesystem",
        #         "/Users/ashwaryjharbade/Projects/pageAnalysisAgent/aidrivenproject",
        #     ]
        # }
    }
)

async def get_tools():
    tools = await mcp_client.get_tools()
    for tool in tools:
        print(tool.name)
        print(tool.description)
    return tools

async def build_agent():
    tools = await get_tools()
    return create_deep_agent(
        model=model,
        tools=tools,
        backend=backend,
        middleware=[
            FilesystemMiddleware(
                backend=backend,
                tools=["read_file", "ls", "glob", "grep"]
            )
        ],
    )

graph = asyncio.run(build_agent())