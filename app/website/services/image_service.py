from ..models.image import Image

from ... import db_context

def delete(id:int):
    """
    Delete an image by Id
    Args:
        id (int): Id of the image

    Returns:
        _type_: True if success else False
    """
    try:
        image = Image.query.get(id)
        if image:
            db_context.session.delete(image)
            db_context.session.commit()
        return True, image.url
    except Exception as e:
        print(e)
        return False, None