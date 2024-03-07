from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, responses, status
from fastapi.templating import Jinja2Templates
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from db.repository.blog import list_blogs, retreive_blog, create_new_blog, delete_blog
from db.session import get_db
from schemas.blog import CreateBlog
from apis.v1.route_login import get_current_user


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def home(request: Request, alert: Optional[str] = None, db: Session = Depends(get_db)):
    blogs = list_blogs(db=db)
    print(alert)
    return templates.TemplateResponse(
        "blog/home.html", {"request": request, "blogs": blogs, "alert": alert}
    )


@router.get("/app/blog/{blog_id}")
def blog_detail(request: Request, blog_id: int, db: Session = Depends(get_db)):
    blog = retreive_blog(blog_id=blog_id, db=db)
    return templates.TemplateResponse(
        "blog/detail.html", {"request": request, "blog": blog}
    )


@router.get("/app/create-new-blog")
def create_blog(request: Request):
    return templates.TemplateResponse("blog/create_blog.html", {"request": request})


@router.post("/app/create-new-blog")
def create_blog(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        author = get_current_user(token=token, db=db)
        blog = CreateBlog(title=title, content=content)
        blog = create_new_blog(blog=blog, db=db, author_id=author.id)
        return responses.RedirectResponse(
            "/?alert=Blog Submitted for Review", status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        errors = ["Please log in to create blog"]
        print("Exception raised", e)
        return templates.TemplateResponse(
            "blog/create_blog.html",
            {"request": request, "errors": errors, "title": title, "content": content},
        )


@router.get("/delete/{blog_id}")
def delete_a_blog(request: Request, blog_id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        author = get_current_user(token=token, db=db)
        msg = delete_blog(blog_id=blog_id, author_id=author.id, db=db)
        alert = msg.get("error") or msg.get("msg")
        return responses.RedirectResponse(
            f"/?alert={alert}", status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        print(f"Exception raised while deleting {e}")
        blog = retreive_blog(blog_id=blog_id, db=db)
        return templates.TemplateResponse(
            "blog/detail.html",
            {"request": request, "alert": "Please Login Again", "blog": blog},
        )
