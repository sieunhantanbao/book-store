from uuid import UUID
from ..schemas.wishlist import WishList
from sqlalchemy.orm import Session

def get_all(db: Session, user_id: UUID):
    """
    Get all wishlist by user_id
    """
    wishlists = db.query(WishList).filter_by(user_id=user_id).all()
    return wishlists

def get_by_user_and_book(db: Session, user_id: UUID, book_id: UUID):
    """
    Get Wishlist by user_id and book_id
    """
    return db.query(WishList).filter_by(user_id=user_id, book_id=book_id).first()

def create(db: Session, user_id: UUID, book_id: UUID):
    """
    Create a wishlist
    """
    try:
        existing_wishlist = get_by_user_and_book(db, user_id, book_id)
        if not existing_wishlist:
            wishlist = WishList(user_id = user_id,
                        book_id = book_id
                        )
            db.add(wishlist)
            db.commit()
        return True
    except:
        return False
    

def delete(db: Session, wishlist_id: UUID):
    """
    Remove a wishlist
    """
    delete = db.delete(WishList).where(id = wishlist_id)
    delete.execute()
    # Update database
    db.commit()

def delete_by_user_and_book(db: Session, user_id, book_id):
    """
    Remove a wishlist by user_id and book_id
    """
    try:
        db.query(WishList).filter_by(user_id = user_id, book_id = book_id).delete()
        # Update database
        db.commit()
        return True
    except Exception as e:
        print(e.message)
        return False