from typing import List

from generate import generate_response, generate_image


# 주제 선정 에이전트
class ThemeSelectionAgent:
    def generate_theme(self, keyword: str) -> str:
        messages = [
            {"role": "system", "content": "너는 특정 키워드에 대해서 주제를 만들어주는 assistant야."},
            {"role": "user", "content": f"'{keyword}' 키워드를 활용해서 짧은 이야기를 만들거야. 이 이야기의 주제를 만들어줘. 주제에는 반드시 키워드를 포함해야해. 부연설명 없이 주제만 하나 생성해줘."}
        ]
        return generate_response(messages)


# 챗봇 에이전트
class ChatBotAgent:
    def generate_sentence(self, theme: str, previous_sentences: List[str]) -> str:
        if not previous_sentences:
            messages = [
                {"role": "system", "content": "너는 특정 주제에 대해서 이야기를 만드는 창의적인 assistant야."},
                {"role": "user", "content": f"주제는 다음과 같아. '{theme}'. 짧은 이야기의 첫 문장을 만들어줘."}
            ]
        else:
            messages = [
                {"role": "system", "content": "너는 특정 주제에 대해서 이야기를 만드는 창의적인 assistant야."},
                {"role": "user", "content": f"주제는 다음과 같아. '{theme}'. 한 문장만 이용해서 다음의 이야기를 계속 이어가줘. (이전 이야기: {' '.join(previous_sentences)}) 이전 이야기는 제외하고 새로 생성한 문장만 출력해."}
            ]
        return generate_response(messages)

# 사람 유저
class HumanUser:
    def __init__(self, name: str):
        self.name = name

    def generate_sentence(self, theme: str, previous_sentences: List[str]) -> str:
        if not previous_sentences:
            input_prompt = f"{self.name}, 주제 '{theme}'에 대해 이야기를 시작하는 첫 문장을 입력해주세요: "
        else:
            input_prompt = f"{self.name}, 주제 '{theme}'에 대해 이야기를 이어갈 문장을 입력해주세요. 현재 이야기: {' '.join(previous_sentences)}\n입력: "
        return input(input_prompt)

# 이미지 에이전트
class SummaryAgent:
    def summarize_story(self, sentences: List[str]) -> str:
        messages = [
            {"role": "system", "content": "너는 창의적이고 트렌디한 짧은 이야기 생성 assistant야"},
            {"role": "user", "content": f"다음 이야기를 기반으로 이미지를 생성할거야. 트렌디한 이미지가 나오도록 프롬프트를 작성해줘. (이야기: {' '.join(sentences)}) 이 이야기는 다시 출력하지 않아도 돼."}
        ]
        return generate_response(messages)
    
    
class ImageAgent:
    def generate_thumbnail(self, summary_prompt):
        return generate_image(summary_prompt)
        