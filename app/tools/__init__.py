from app.tools.web_tools import WebTools


def get_all_tools():
    """Aggregates all tools from different providers."""
    web = WebTools()

    # In the future, you can add more tool providers here:
    # database = DatabaseTools()
    # return web.get_tools() + database.get_tools()

    return web.get_tools()
