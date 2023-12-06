from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_username(request: Request):
    username = request.cookies.get("username")
    return username


@app.get("/")
def main_page(request: Request):
    query = request.query_params.get("query")
    if not query:
        return templates.TemplateResponse("main_page.html", {"request": request})
    else:
        message = f"Sorry, no results were found for <b>{query}</b>. <a href='?'>Try again</a>."
        return templates.TemplateResponse(
            "results.html", {"request": request, "message": message}
        )


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(response: Response, username: str = Form(...), password: str = Form(...)):
    # Validate username and password here...
    # If valid, set the username and password in a cookie
    response.set_cookie(key="username", value=username)
    response.set_cookie(key="password", value=password)
    return RedirectResponse(url="/protected")


@app.get("/protected")
async def protected_page(request: Request, username: str = Depends(get_username)):
    if username:
        return templates.TemplateResponse(
            "protected_page.html", {"request": request, "username": username}
        )
    else:
        return RedirectResponse(url="/")


@app.get("/static/{file_path}")
async def static_file(file_path: str):
    # Serve static files, update the base directory path according to your file structure
    return FileResponse(f"static/{file_path}")
