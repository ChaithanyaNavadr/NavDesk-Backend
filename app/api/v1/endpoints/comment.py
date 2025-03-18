from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentResponse
from app.models.ticket import Ticket

router = APIRouter()

# ✅ Create a new comment
@router.post("/", response_model=CommentResponse)
def create_comment(comment_data: CommentCreate, db: Session = Depends(get_db)):
    # Check if the associated ticket exists
    ticket = db.query(Ticket).filter(Ticket.ticket_id == comment_data.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    new_comment = Comment(text=comment_data.text, ticket_id=comment_data.ticket_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# ✅ Get all comments
@router.get("/", response_model=list[CommentResponse])
def get_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()

# ✅ Get a specific comment by ID
@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

# ✅ Update a comment
@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.text = comment_data.text
    db.commit()
    db.refresh(comment)
    return comment

# ✅ Delete a comment
@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
