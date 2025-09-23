from app.main.config import process_data
from app.model.gen_label import generate_place_label


def gen_prompt():

    user_image, event = process_data()
    place = generate_place_label()


    prompt = f"""

    Generate an image of a person doing "{event}" at {place}.
    The image should be in a realistic style with high detail and vibrant colors.

    """

    return prompt