from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, HTTPException
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from db.session import get_db
from db.repository.blog import create_new_blog, retreive_blog, list_blogs, update_blog, delete_blog


router = APIRouter()


@router.post("/blogs", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    blog = create_new_blog(blog=blog, db=db, author_id=1)
    return blog


@router.get("/blogs/{blog_id}", response_model=ShowBlog)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = retreive_blog(blog_id=blog_id, db=db)
    if not blog:
        raise HTTPException(detail=f"Blog with ID {blog_id} does not exist.", status_code=status.HTTP_404_NOT_FOUND)
    return blog


@router.get("/blogs", response_model=List[ShowBlog])
def get_blogs(db: Session = Depends(get_db)):
    blogs = list_blogs(db=db)
    return blogs


@router.put("/blogs/{blog_id}", response_model=ShowBlog)
def update_a_blog(blog_id: int, blog: UpdateBlog, db: Session = Depends(get_db)):
    blog = update_blog(blog_id=blog_id, blog=blog, db=db)
    if not blog:
        raise HTTPException(detail=f"Blog with ID {id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    return blog


@router.delete("/blogs/{blog_id}")
def delete_a_blog(blog_id: int, db: Session = Depends(get_db)):
    message = delete_blog(blog_id=blog_id, author_id=1, db=db)
    if message.get("error"):
        raise HTTPException(detail=message.get("error"), status_code=status.HTTP_400_BAD_REQUEST)
    return {"status": 0}
