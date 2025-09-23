from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from app.main.config import process_data
import warnings
import logging

load_dotenv()

def generate_place_label():
    user_image, event = process_data()

    prompt = f"""
    Generate exactly ONE word that best describes the background or setting where the event "{event}" typically takes place.

    Examples:
    - If event is "cricket" → output: "ground"
    - If event is "movie" → output: "cinema" 
    - If event is "concert" → output: "stage"
    - If event is "wedding" → output: "venue"
    - If event is "cooking" → output: "kitchen"

    Event: {event}
    Output only the single word, nothing else:
    """
    
    llm = GoogleGenerativeAI(model="gemini-2.0-flash-lite")
    result = llm.invoke(prompt)
    logging.info("Label Generation Result: %s", result)
    return result

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    label = generate_place_label()
    print(f"Generated Label: {label}")