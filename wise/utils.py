from datetime import datetime

from markdown import Markdown
from telegraph import Telegraph


def create_page(content: str = "this is content"):
    telegraph = Telegraph()
    telegraph.create_account(short_name="Wise Bot")

    contents = [
        datetime.now().isoformat(),
        content,
    ]

    md = Markdown().set_output_format("html")
    resp = telegraph.create_page(
        title="Wise Fee",
        html_content=md.convert("\n\n".join(contents)),
    )
    return resp
