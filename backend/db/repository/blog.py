from db.models.blog import Blog
from schemas.blog import CreateBlog
from schemas.blog import UpdateBlog
from sqlalchemy.orm import Session


def create_new_blog(blog: CreateBlog, db: Session, author_id: int = 1):
    blog = Blog(**blog.dict(), author_id=author_id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def retreive_blog(blog_id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    return blog


def list_blogs(db: Session):
    blogs = db.query(Blog).filter(Blog.is_active == True).all()
    return blogs


def update_blog(blog_id: int, blog: UpdateBlog, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog_in_db:
        return {"error": f"Blog with id {blog_id} does not exist"}
    if not blog_in_db.author_id == author_id:
        return {"error": "Only the author can modify the blog"}
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    db.add(blog_in_db)
    db.commit()
    return blog_in_db


def delete_blog(blog_id: int, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog_in_db:
        return {"error": f"Could not find blog with id {blog_id}"}
    if blog_in_db.author_id != author_id:
        return {"error": "Only the author can delete a blog"}
    db.delete(blog_in_db)
    db.commit()
    return {"msg": f"Successfully deleted blog with id {blog_id}"}
