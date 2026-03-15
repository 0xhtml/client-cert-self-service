"""Allow users to self service a client cert."""

import jinja2
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

_TEMPLATES = Jinja2Templates(
    env=jinja2.Environment(
        autoescape=True,
        loader=jinja2.FileSystemLoader("templates"),
        lstrip_blocks=True,
        trim_blocks=True,
    ),
)


def _template_response(
    request: Request,
    template_name: str,
    context: dict[str, object],
) -> Response:
    if "HX-Request" in request.headers:
        context["base"] = "htmx.html"
    else:
        context["base"] = "base.html"
    return _TEMPLATES.TemplateResponse(
        request,
        template_name,
        context,
        headers={"Vary": "HX-Request, HX-Target"},
    )


def _index(request: Request) -> HTMLResponse:
    return _template_response(request, "index.html", {"title": "Register"})


app = Starlette(
    routes=[
        Route("/", endpoint=_index),
        Mount("/static", app=StaticFiles(directory="static"), name="static"),
    ],
)
