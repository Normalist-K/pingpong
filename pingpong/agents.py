import os
from typing import List
import json

from generate import generate_response, generate_image


class PromptLoader:
    def __init__(self, base_path=None):
        if base_path is None:
            base_path = self.find_project_root()
        self.prompt_dir = os.path.join(base_path, 'prompt')
        self.prompts = {}
        self.load_all_prompts()

    def find_project_root(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while True:
            if os.path.exists(os.path.join(current_dir, '.project-root')):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                raise FileNotFoundError("'.project-root' 파일을 찾을 수 없습니다. 프로젝트 루트에 이 파일을 생성해주세요.")
            current_dir = parent_dir

    def load_all_prompts(self):
        for filename in os.listdir(self.prompt_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.prompt_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.prompts[filename[:-5]] = json.load(f)

    def get_first_sentence_prompt_by_author(self, author_name: str):
        authors = self.prompts.get('author_styles', {})
        author = authors.get(author_name)
        if author:
            prompt = f"""
                특정 키워드가 제시될거에요. 
                그러면 소설가 {author_name}의 문체로 사용하여 짧은 이야기의 첫 문장을 만들어주세요 \n 
                문체: {author.get('style')}
                """
        else:
            prompt = f"""
                특정 키워드가 제시될거에요. 
                그러면 소설가 {author_name}의 문체로 사용하여 짧은 이야기의 첫 문장을 만들어주세요.
                """
        return prompt
    
    def get_first_sentence_prompt_by_style(self, style_name: str):
        styles = self.prompts.get('writing_styles', {})
        style = styles.get(style_name)
        if style:
            prompt = f"""
                특정 키워드가 제시될거에요. 
                그러면 아래 문체로 짧은 이야기의 첫 문장을 만들어주세요 \n 
                [문체: {style.get('style')}]
                """
        else:
            prompt = """
                특정 키워드가 제시될거에요. 
                그러면 소설가의 문체로 짧은 이야기의 첫 문장을 만들어주세요.
                """
        return prompt
        
    def get_author_style_prompt(self, author_name: str):
        authors = self.prompts.get('author_styles', {})
        author = authors.get(author_name)
        if author:
            prompt =  f"""
                특정 키워드가 제시될거에요. 
                그러면 소설가 {author_name}의 문체로 사용하여 짧은 이야기를 만들거에요. 
                이전 이야기를 참고해서 이어가주세요. \n 
                문체: {author.get('style')}
                """
        else:
            prompt = """
                특정 키워드가 제시될거에요. 
                그러면 소설가의 문체로 사용하여 짧은 이야기를 만들거에요. 
                이전 이야기를 참고해서 이어가주세요.
                """
        return prompt
    
    def get_writing_style_prompt(self, writing_style: str):
        styles = self.prompts.get('writing_styles', {})
        style = styles.get(writing_style)
        if style:
            prompt = f"""
                특정 키워드가 제시될거에요. 
                그러면 아래 문체로 짧은 이야기를 만들거에요. \n 
                이전 이야기를 참고해서 이어가주세요. \n 
                [문체: {style.get('style')}]
                """
        else:
            prompt = """
                특정 키워드가 제시될거에요. 
                그러면 소설 문체로 짧은 이야기를 만들거에요. \n 
                이전 이야기를 참고해서 이어가주세요. \n 
                """
        return prompt


# 첫문장 생성 에이전트
class FirstSentenceAgent:
    def __init__(self):
        self.prompt_loader = PromptLoader()
        
    def generate_sentence(self, keyword: str, writing_style: str = None) -> str:
        writing_style_prompt = self.prompt_loader.get_first_sentence_prompt_by_style(writing_style)
        messages = [
            {"role": "system", "content": writing_style_prompt},
            {"role": "user", "content": f"""
                아래 키워드로 짧은 이야기의 첫 문장을 만들어줘.\n
                [키워드: {keyword}]
            """}
        ]
        return generate_response(messages)


class ChatBotAgent:
    def __init__(self):
        self.prompt_loader = PromptLoader()

    def generate_sentence(self, keyword: str, previous_sentences: List[str], writing_style: str = None) -> str:
        writing_style_prompt = self.prompt_loader.get_writing_style_prompt(writing_style)
        messages = [
            {"role": "system", "content": writing_style_prompt},
            {"role": "user", "content": f"""
                한 문장만 이용해서 다음의 이야기를 계속 이어가줘. 이전 이야기는 제외하고 새로 생성한 문장만 출력해. \n
                [키워드: {keyword}] \n
                [이전 이야기: {' '.join(previous_sentences)}]
            """}
        ]
        return generate_response(messages)

# 사람 유저
class HumanUser:
    def __init__(self, name: str):
        self.name = name

    def generate_sentence(self, keyword: str, previous_sentences: List[str]) -> str:
        if not previous_sentences:
            input_prompt = f"{self.name}, 키워드 '{keyword}'에 대해 이야기를 시작하는 첫 문장을 입력해주세요: "
        else:
            input_prompt = f"{self.name}, 키워드 '{keyword}'에 대해 이야기를 이어갈 문장을 입력해주세요. 현재 이야기: {' '.join(previous_sentences)}\n입력: "
        return input(input_prompt)

# 프롬프트 서머리 에이전트
class SummaryAgent:
    def summarize_story(self, sentences: List[str]) -> str:
        messages = [
            {"role": "system", "content": "너는 창의적이고 트렌디한 짧은 이야기 생성 assistant야"},
            {"role": "user", "content": f"다음 이야기를 기반으로 이미지를 생성할거야. 트렌디한 이미지가 나오도록 프롬프트를 작성해줘. (이야기: {' '.join(sentences)}) 이 이야기는 다시 출력하지 않아도 돼."}
        ]
        return generate_response(messages)
    
# 이미지 에이전트
class ImageAgent:
    def generate_thumbnail(self, summary_prompt):
        return generate_image(summary_prompt)
        
        
        
# 파일 끝에 다음 코드 추가
if __name__ == "__main__":
    # PromptLoader 인스턴스 생성
    loader = PromptLoader()
    
    # 로드된 모든 프롬프트 출력
    print("로드된 모든 프롬프트:")
    for key, value in loader.prompts.items():
        print(f"{key}: {value}")
    
    # 특정 스타일의 첫 문장 프롬프트 가져오기
    style_name = "유머러스한"  # 예시 스타일 이름
    style_prompt = loader.get_first_sentence_prompt_by_style(style_name)
    print(f"\n{style_name} 스타일의 첫 문장 프롬프트:")
    print(style_prompt)