from app.main.config import process_data
from app.model.label_gen import generate_place_label


def gen_prompt():

    user_image, event = process_data()
    place = generate_place_label()


    prompt = f"""

    Generate an image of a person doing "{event}" at {place}.
    The image should be in a realistic style with high detail and vibrant colors.
    Try to match the person's appearance as possible to the provided image but clothing can be varied, depends on the {place}.

    """

    return prompt