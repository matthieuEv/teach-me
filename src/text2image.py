import requests
from dotenv import load_dotenv
import os
import base64
import time

load_dotenv()

def generate_picture(prompt, index):
    invoke_url = "https://ai.api.nvidia.com/v1/genai/briaai/bria-2.3"

    headers = {
        "Authorization": f'Bearer {os.getenv("OPENAI_API_KEY")}',
        "Accept": "application/json",
    }

    payload = {
        "prompt": prompt,
        "cfg_scale": 5,
        "aspect_ratio": "16:9",
        "seed": 0,
        "steps": 30,
        "negative_prompt": ""
    }

    while True:
        try:
            response = requests.post(invoke_url, headers=headers, json=payload)
            response.raise_for_status()  # This will raise an HTTPError for bad responses

            response_body = response.json()
            base64_img = response_body["image"]

            current_path = os.getcwd()
            output_path = os.path.join(current_path, "data", str(index) + ".jpg")

            save_base64_image_as_jpeg(base64_img, output_path)
            return f"Image saved at {output_path}"

        except requests.exceptions.HTTPError as err:
            if response.status_code == 500:
                print("Server error 500, retrying in 1 second...")
                time.sleep(1)
            else:
                raise err  # Re-raise the exception if it's not a 500 error

def save_base64_image_as_jpeg(base64_img, output_path):
    img_data = base64.b64decode(base64_img)
    with open(output_path, "wb") as f:
        f.write(img_data)
    print(f"Image saved at {output_path}")

if __name__ == "__main__":
    prompt = input("Enter the prompt: ")
    generate_picture(prompt, 2)
