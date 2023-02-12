from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response
from sqlalchemy import func
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def index(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
          limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).all()
    # cur.execute("""SELECT * FROM posts """)
    # posts = cur.fetchall()
    # print(posts)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def store(post: schemas.PostCreate, db: Session = Depends(get_db),
          current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute(f"") cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    # (post.title, post.content, post.published)) new_post = cur.fetchone() conn.commit() post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000) my_posts.append(post_dict) print(post) print(post.dict())
    print(current_user)
    new_post = models.Post(**post.dict(), owner_id=current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# guardar collection en postman 1:38:25
@router.get("/{id}", response_model=schemas.PostOut)
def show(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post1 = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE id= %s RETURNING * """, (str(id),))
    # deleted_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id).first()
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db),
           current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""UPDATE posts SET title = %s, content= %s, published=%s WHERE id = %s RETURNING *""",
    #            (post.title, post.content, post.published, str(id)))
    # updated_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
