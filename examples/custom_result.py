from flogin import ExecuteResponse, Plugin, Query, Result

plugin = Plugin()


class MyResult(Result):
    async def callback(self):
        """Handle what happens when the user clicks on the result"""

        await plugin.api.show_notification("Flogin", "I work!")
        return ExecuteResponse(hide=False)

    async def on_error(self, error: Exception):
        """Handle errors from the 'callback' method"""

        await plugin.api.show_error_message(
            "Flogin",
            f"An error has occured while executing the result's callback: {error}",
        )
        return ExecuteResponse(hide=False)

    async def context_menu(self):
        """Generate this result's context menu"""

        return Result("This is a test")

    async def on_context_menu_error(self, error: Exception):
        """Handle errors from the 'context_menu' method"""

        return f"An error has occured: {error}"


@plugin.search()
async def on_search(data: Query):
    return MyResult("This is my result")


if __name__ == "__main__":
    plugin.run()
