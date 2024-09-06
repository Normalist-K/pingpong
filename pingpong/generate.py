import requests

from openai import OpenAI

client = OpenAI()


# OpenAI API를 통해 문장을 생성하는 함수
def generate_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt
    )
    return response.choices[0].message.content.strip()


def generate_image(prompt: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,  # 이미지 프롬프트를 활용
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    image_url = response.data[0].url
    image_data = requests.get(image_url)
    
    assert image_data.status_code == 200, f"Failed to retrieve image. HTTP Status code: {image_data.status_code}"

    return image_data