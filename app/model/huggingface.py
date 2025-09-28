import os
from huggingface_hub import InferenceClient
from PIL import Image
from huggingface_hub.inference._generated.types.image_to_image import ImageToImageTargetSize
from dotenv import load_dotenv
from app.model.prompt import gen_prompt
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

def image_editing():

    image_prompt = gen_prompt()

    os.makedirs("./data/user_image", exist_ok=True)
    os.makedirs("./data/generated_image", exist_ok=True)

    subject_image = "./data/user_image/image.jpg"
    output_dir = "./data/generated_image"

    client = InferenceClient(
        provider="auto",
        api_key=os.environ["HF_TOKEN"],
    )

    user_image = Image.open(subject_image)

    # output is a PIL.Image object
    for interation in range(1):
        image = client.image_to_image(
            user_image,
            prompt=image_prompt,
            model="black-forest-labs/FLUX.1-Kontext-dev",
            target_size=ImageToImageTargetSize(width=512, height=512),
        )

        image.save(f"{output_dir}/v{interation}.png")

    logging.info("Image Generation Done!")

if __name__ == "__main__":
    image_editing()