from quart import render_template


async def flash(status: str, msg: str, template: str) -> str:
    """Flashes a success/error message on a specified template."""
    return await render_template(f'{template}.html', flash=msg, status=status)
