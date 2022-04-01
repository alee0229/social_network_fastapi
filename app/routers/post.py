from .. import models, schemas, database, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    )
#______________________________________________________ POST______________________________________________________________________

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db),
                 current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #RAW SQL
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    #SQLALCHEMY // ORM
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #SELECT posts.*, COUNT(votes.post_id) FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(
                                                models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
#RAW SQL
#    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s,%s,%s) RETURNING * """,
#                     (post.title, post.content, post.published))
#    new_post = cursor.fetchone()
#    conn.commit()

#SQLALCHEMY // ORM
# **post.dict() unpacks the dictionary to title=post.title, content= post.content
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id,
        **post.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# title str, content str

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(database.get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
#RAW SQL
    # cursor.execute(""" SELECT * FROM posts WHERE id =%s""", (str(id),))
    # post = cursor.fetchone()

#SQLALCHEMY // ORM
    # posts = db.query(models.Post).filter(models.Post.id == id).first()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                models.Vote.post_id == models.Post.id, isouter= True).group_by(
                                                models.Post.id).filter(models.Post.id == id).first()
    if not posts:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    return posts


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
#RAW SQL
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

#SQLALCHEMY // ORM
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id) 

    deleted_post = deleted_post_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
#RAW SQL
    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",
    #     (post.title,post.content, post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

#SQLALCHEMY // ORM
    updated_post_query = db.query(models.Post).filter(models.Post.id == id) 

    updated_post = updated_post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    updated_post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return updated_post
