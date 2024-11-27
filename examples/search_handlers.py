from flogin import Plugin, Query, Result, SearchHandler

plugin = Plugin()


class MyHandler(SearchHandler):
    async def callback(self, query: Query):
        return f"This comes from my subclassed handler"

    async def on_error(self, error: Exception):
        """Handle errors from the 'callback' method"""
        return f"An error occured: {error}"


@plugin.search()
async def my_simple_search_handler(data: Query):
    return f"This comes from my simple handler"


@my_simple_search_handler.error
async def my_simple_search_handler_error_handler(error: Exception):
    """Handle errors in my 'my_simple_search_handler'"""
    return f"An error occured: {error}"


if __name__ == "__main__":
    plugin.run()
