import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from app.model.prompt import gen_prompt
import logging

load_dotenv()

def image_editing():

    image_prompt = gen_prompt()

    os.makedirs("./data/user_image", exist_ok=True)
    os.makedirs("./data/generated_image", exist_ok=True)

    subject_image = "./data/user_image/image.jpg"
    output_dir = "./data/generated_image"

    client = InferenceClient(
        provider="fal-ai",
        api_key=os.environ["HF_TOKEN"],
    )

    with open(subject_image, "rb") as image_file:
        input_image = image_file.read()

    # output is a PIL.Image object
    for interation in range(1):
        image = client.image_to_image(
            input_image,
            prompt=image_prompt,
            model="black-forest-labs/FLUX.1-Kontext-dev",
        )

        image.save(f"{output_dir}/v{interation}.png")
    logging.info("Image Generation Done!")

if __name__ == "__main__":
    image_editing()