import requests

from openai import OpenAI

client = OpenAI()

api_call_logs = []

def get_api_call_logs():
    global api_call_logs
    return api_call_logs

def reset_api_call_logs():
    global api_call_logs
    api_call_logs = []

# OpenAI API를 통해 문장을 생성하는 함수
def generate_response(messages):
    global api_call_logs
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    api_call_logs.append({"type": "text", "messages": messages})
    return response.choices[0].message.content.strip()

def generate_image(prompt):
    global api_call_logs
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,  # 이미지 프롬프트를 활용
        size="1024x1024",
        quality="standard",
        n=1,
    )
    api_call_logs.append({"type": "image", "prompt": prompt})

    image_url = response.data[0].url
    image_data = requests.get(image_url)
    assert image_data.status_code == 200, f"Failed to retrieve image. HTTP Status code: {image_data.status_code}"

    return image_data