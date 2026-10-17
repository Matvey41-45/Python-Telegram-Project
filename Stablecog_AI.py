import requests
import os
import config

headers = {
    'Authorization': f'Bearer {config.SECRET_KEY}',
    'Content-Type': 'application/json'
}

URL = 'https://api.stablecog.com/v1/image/generation/create'

def generate(prompt):
    response = requests.post(
        URL,
        json={"prompt": prompt},
        headers=headers
    )

    data = response.json()
    os.makedirs("images", exist_ok=True)
    saved_files = []

    for output in data.get("outputs", []):
        image_url = output["image_url"]
        image_id = output.get("id", "image")

        filename_part = image_url.split('/')[-1]
        filename_part = filename_part.strip()
        extension = os.path.splitext(filename_part)[1]

        filename = f"{image_id}{extension}"
        filepath = os.path.join("images", filename)

        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(img_response.content)
            saved_files.append(filepath)

    return saved_files