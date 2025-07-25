from dotenv import load_dotenv
from openai import OpenAI

# Load API key from environment variable
load_dotenv()

client = OpenAI()

# Upload image using OpenAI Files API
def upload_image(file_path):
    with open(file_path, "rb") as f:
        result = client.files.create(file=f, purpose="user_data")
        return result.id

def main():
    #image_path = "SA20250410-5395-123-336.png"
    image_path = "test.jpg"
    file_id = upload_image(image_path)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "what's in this image?"},
                {
                    "type": "input_image",
                    "file_id": file_id,
                },
            ],
        }],
    )
    print(response.output_text)

if __name__ == "__main__":
    main()


 