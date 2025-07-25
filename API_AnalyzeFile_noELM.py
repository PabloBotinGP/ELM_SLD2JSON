from dotenv import load_dotenv
from openai import OpenAI
import time

# Load API key from environment variable
load_dotenv()

client = OpenAI()

# Upload image using OpenAI Files API
def upload_image(file_path):
    with open(file_path, "rb") as f:
        result = client.files.create(file=f, purpose="user_data")
        return result.id

def main():
    
    # Upload file and store file_id. 
    image_path = "diagram.jpg"
    file_id = upload_image(image_path)

    # === First interaction (with image) ===
    response1 = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "What’s in this image?"},
                {"type": "input_image", "file_id": file_id},
            ],
        }]
    )

    print("=== Response 1 ===")
    print(response1.output_text)

    # Optional delay for clarity
    time.sleep(1)

    # === Second interaction (text only, relies on context) ===
    response2 = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Do you still have access to the image I uploaded in the previous call?"}
            ],
        }]
    )

    print("\n=== Response 2 ===")
    print(response2.output_text)

    # === Third interaction ===
    response3 = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Which inverter model is used?"}
            ],
        }]
    )

    print("\n=== Response 3 ===")
    print(response3.output_text)

if __name__ == "__main__":
    main()