import os
import random
from datetime import datetime
from pprint import pprint
from typing import List, Union

from agents import ChatBotAgent, HumanUser, ThemeSelectionAgent, SummaryAgent, ImageAgent


# 게임 클래스
class StoryGame:
    def __init__(
            self, 
            participants: List[Union[ChatBotAgent, HumanUser]], 
            max_turns: int = 4, 
            termination_msg: str = "The End",
            gen_img:bool = True
        ):
        self.participants = participants
        self.max_turns = max_turns
        self.termination_msg = termination_msg
        self.gen_img = gen_img
        self.sentences = []
        
        if self.gen_img:
            self.image_agent = ImageAgent()

    def start_game(self, keyword: str):
        # 1. 주제 선정
        theme_agent = ThemeSelectionAgent()
        theme = theme_agent.generate_theme(keyword)
        print(f"Selected Theme: {theme}")

        # 2. 첫 문장 생성
        first_participant = random.choice(self.participants)
        first_sentence = first_participant.generate_sentence(theme, [])
        self.sentences.append(first_sentence)
        print(f"First Sentence: {first_sentence}")

        # 이미 턴을 마친 참가자를 저장할 리스트
        participants_done = [first_participant]

        # 3. 참여자들이 돌아가며 이야기 진행
        turn = 0
        while turn < self.max_turns:
            if len(participants_done) == len(self.participants):
                participants_done = []  # 모든 참가자가 턴을 완료하면 리스트 초기화

            # 현재 턴에서 참가할 참가자 선택 (이미 턴을 마친 참가자는 제외)
            remaining_participants = [p for p in self.participants if p not in participants_done]
            current_participant = random.choice(remaining_participants)

            # 문장 생성
            sentence = current_participant.generate_sentence(theme, self.sentences)
            self.sentences.append(sentence)
            print(f"Turn {turn}: {sentence}")

            # 현재 참가자를 완료 리스트에 추가
            participants_done.append(current_participant)

            # 종료 조건 체크
            if self.termination_msg in sentence:
                break

            turn += 1

        # 4. 서머리 에이전트가 이야기를 바탕으로 이미지 생성 프롬프트를 작성
        summary_agent = SummaryAgent()
        self.summary_prompt = summary_agent.summarize_story(self.sentences)
        print("\nFinal Story:")
        pprint(self.sentences)
        print("\nSummary:")
        pprint(self.summary_prompt)

        # 5. 서머리 프롬프트를 바탕으로 이미지 생성
        if self.gen_img:
            self.img = self.image_agent.generate_thumbnail(self.summary_prompt)

        # 6. 결과 저장
        self.save_results()

    def save_results(self):
        # 저장 디렉토리 설정
        now = datetime.now()
        save_dir = os.path.join("./results", now.strftime("%Y%m%d_%H%M%S"))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        # 이야기 저장
        txt_path = os.path.join(save_dir, f'{now.strftime("%Y%m%d_%H%M%S")}.txt')
        with open(txt_path, 'w') as file:
            for line in self.sentences:
                file.write(line + '\n')
            file.write(f'\n{self.summary_prompt}')
        print(f"Story has been saved in {txt_path}")

        # 이미지 저장
        if self.gen_img:
            img_path = os.path.join(save_dir, f'{now.strftime("%Y%m%d_%H%M%S")}.jpg')
            with open(img_path, 'wb') as file:
                file.write(self.img.content)
        print(f"Image has been saved in {img_path}")