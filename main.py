
from dotenv import load_dotenv
import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from deepagents.backends import FilesystemBackend
from deepagents import FilesystemPermission, create_deep_agent
from deepagents.middleware import FilesystemMiddleware
from langchain.tools import tool
from models import model

load_dotenv()
CONTEXT7_API_KEY = os.getenv("CONTEXT7_API_KEY")

backend = FilesystemBackend(
    root_dir="./workspace-container",
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
        #         "/Users/ashwaryjharbade/Projects/pageAnalysisAgent/workspace-container",
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

@tool
def fetch_file(path: str) -> str:
    """Read a file from the filesystem."""
    return f"Contents of {path}"

async def build_agent():
    tools = await get_tools()
    return create_deep_agent(
        model=model,
        tools=[fetch_file] + tools,
        backend=backend,
        permissions=[
            FilesystemPermission(
                operations=["write"],
                paths=["/workspace/**"],
                mode="allow",
            ),
            FilesystemPermission(
                operations=["ls"],
                paths=["/skills/**"],
                mode="deny",
            ),
            FilesystemPermission(
                operations=["write"],
                paths=["/**"],
                mode="deny",
            )
        ],
        middleware=[
            FilesystemMiddleware(
                backend=backend,
                tools=["read_file", "ls", "glob", "grep", "write_file"]
            )
        ],
        skills=["./workspace-container/skills/"],
        # interrupt_on={
        #     "fetch_file": { "allowed_decisions": ["approve", "reject"] }
        # }
    )

graph = asyncio.run(build_agent())