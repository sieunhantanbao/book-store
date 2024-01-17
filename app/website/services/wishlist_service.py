from ..models.wishlist import WishList
from ... import db_context

def get_all(user_id):
    """
    Get all wishlist by user_id
    """
    wishlists = WishList.query.filter_by(user_id=user_id).all()
    return wishlists

def get_by_user_and_book(user_id, book_id):
    """
    Get Wishlist by user_id and book_id
    """
    return WishList.query.filter_by(user_id=user_id, book_id=book_id).first()

def create(user_id, book_id):
    """
    Create a wishlist
    """
    try:
        existing_wishlist = get_by_user_and_book(user_id, book_id)
        if not existing_wishlist:
            wishlist = WishList(user_id = user_id,
                        book_id = book_id
                        )
            db_context.session.add(wishlist)
            db_context.session.commit()
        return True
    except:
        return False
    

def delete(wishlist_id):
    """
    Remove a wishlist
    """
    delete = WishList.delete().where(id = wishlist_id)
    delete.execute()
    # Update database
    db_context.session.commit()

def delete_by_user_and_book(user_id, book_id):
    """
    Remove a wishlist by user_id and book_id
    """
    try:
        WishList.query.filter_by(user_id = user_id, book_id = book_id).delete()
        # Update database
        db_context.session.commit()
        return True
    except Exception as e:
        print(e.message)
        return False