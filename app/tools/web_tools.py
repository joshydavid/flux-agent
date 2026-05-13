from mcp import StdioServerParameters, stdio_client
from strands.tools.mcp import MCPClient


class WebTools:
    """Provides web-related tools using MCP."""

    def __init__(self):
        self.fetch_client = MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="uvx", args=["--quiet", "mcp-server-fetch"]
                )
            )
        )

    def get_tools(self):
        """Returns the list of tools provided by this class."""
        return [self.fetch_client]
