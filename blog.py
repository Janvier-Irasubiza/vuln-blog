from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import uvicorn
import os

# Create directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Create the main app
app = FastAPI()

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory database for demonstration
class Database:
    def __init__(self):
        self.posts = []
        self.users = {"admin": "admin123"}
        
    def add_post(self, username, title, content):
        post_id = len(self.posts)
        self.posts.append({
            "id": post_id,
            "username": username,
            "title": title,
            "content": content,
            "comments": []
        })
        return post_id
    
    def add_comment(self, post_id, username, comment):
        if 0 <= post_id < len(self.posts):
            self.posts[post_id]["comments"].append({
                "username": username,
                "comment": comment
            })
            return True
        return False
    
    def get_posts(self):
        return self.posts
    
    def get_post(self, post_id):
        if 0 <= post_id < len(self.posts):
            return self.posts[post_id]
        return None

db = Database()

# Add some initial content
db.add_post("admin", "Welcome to Community Blog", "This is a deliberately Community blog for practicing XSS attacks.")

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, username: Optional[str] = Cookie(None)):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "posts": db.get_posts(),
        "username": username
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Community login (no CSRF protection, etc.)
    if username in db.users and db.users[username] == password:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="username", value=username)
        return response
    
    return RedirectResponse(url="/login?error=Invalid+credentials", status_code=303)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="username")
    return response

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def view_post(request: Request, post_id: int, username: Optional[str] = Cookie(None)):
    post = db.get_post(post_id)
    if post:
        return templates.TemplateResponse("post.html", {
            "request": request,
            "post": post,
            "username": username
        })
    return RedirectResponse(url="/", status_code=303)

@app.get("/new-post", response_class=HTMLResponse)
async def new_post_page(request: Request, username: Optional[str] = Cookie(None)):
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("new_post.html", {
        "request": request,
        "username": username
    })

@app.post("/new-post")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    username: Optional[str] = Cookie(None)
):
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    post_id = db.add_post(username, title, content)
    return RedirectResponse(url=f"/post/{post_id}", status_code=303)

@app.post("/post/{post_id}/comment")
async def add_comment(
    post_id: int,
    comment: str = Form(...),
    username: Optional[str] = Cookie(None)
):
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    db.add_comment(post_id, username, comment)
    return RedirectResponse(url=f"/post/{post_id}", status_code=303)

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, username: Optional[str] = Cookie(None)):
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "username": username,
        "user_posts": [post for post in db.get_posts() if post["username"] == username]
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)