import os
import random
import json
from datetime import datetime
from pprint import pprint
from typing import List, Union, Optional

from agents import ChatBotAgent, HumanUser, SummaryAgent, ImageAgent, FirstSentenceAgent
from generate import get_api_call_logs, reset_api_call_logs
from utils import get_commit_info

# 게임 클래스
class StoryGame:
    def __init__(
            self, 
            participants: List[Union[ChatBotAgent, HumanUser]], 
            max_turns: int = 4, 
            termination_msg: str = "The End",
            gen_img: bool = True,
        ):
        self.participants = participants
        self.max_turns = max_turns
        self.termination_msg = termination_msg
        self.gen_img = gen_img
        self.sentences: List[str] = []
        self.summary_prompt: Optional[str] = None
        self.img: Optional[bytes] = None
        self.first_sentence_agent = FirstSentenceAgent()

        if self.gen_img:
            self.image_agent = ImageAgent()

        self.log_data = {
            "commit_info": get_commit_info(),
            "game_info": {
                "participants": [type(p).__name__ for p in participants],
                "max_turns": max_turns,
                "termination_msg": termination_msg,
                "gen_img": gen_img,
            },
            "api_calls": [],
        }

    def start_game(self, keyword: str, writing_style: str = None) -> None:
        reset_api_call_logs()  # 게임 시작 시 API 호출 로그 초기화
        self._generate_first_sentence(keyword, writing_style)
        self._generate_story(keyword, writing_style)
        self._generate_summary()
        if self.gen_img:
            self._generate_image()
        self._save_results()
        self._save_log()

    def _generate_first_sentence(self, keyword: str, writing_style: str) -> None:
        first_sentence = self.first_sentence_agent.generate_sentence(keyword, writing_style)
        self.sentences.append(first_sentence)
        print(f"첫 문장: {first_sentence}")

    def _generate_story(self, keyword: str, writing_style: str) -> None:
        participants_done: List[Union[ChatBotAgent, HumanUser]] = []
        
        for turn in range(self.max_turns):
            if len(participants_done) == len(self.participants):
                participants_done = []  # 모든 참가자가 턴을 완료하면 리스트 초기화

            current_participant = self._select_next_participant(participants_done)
            sentence = current_participant.generate_sentence(keyword, self.sentences, writing_style)
            self.sentences.append(sentence)
            print(f"턴 {turn}: {sentence}")

            participants_done.append(current_participant)

            if self.termination_msg in sentence:
                break

    def _select_next_participant(self, participants_done: List[Union[ChatBotAgent, HumanUser]]) -> Union[ChatBotAgent, HumanUser]:
        remaining_participants = [p for p in self.participants if p not in participants_done]
        return random.choice(remaining_participants)

    def _generate_summary(self) -> None:
        summary_agent = SummaryAgent()
        self.summary_prompt = summary_agent.summarize_story(self.sentences)
        print("\n최종 이야기:")
        pprint(self.sentences)
        print("\n요약:")
        pprint(self.summary_prompt)

    def _generate_image(self) -> None:
        self.img = self.image_agent.generate_thumbnail(self.summary_prompt)

    def _save_results(self) -> None:
        save_dir = self._create_save_directory()
        self._save_story(save_dir)
        if self.gen_img:
            self._save_image(save_dir)

    def _create_save_directory(self) -> str:
        now = datetime.now()
        save_dir = os.path.join("./results", now.strftime("%Y%m%d_%H%M%S"))
        os.makedirs(save_dir, exist_ok=True)
        return save_dir

    def _save_story(self, save_dir: str) -> None:
        now = datetime.now()
        txt_path = os.path.join(save_dir, f'{now.strftime("%Y%m%d_%H%M%S")}.txt')
        with open(txt_path, 'w') as file:
            for line in self.sentences:
                file.write(line + '\n')
            file.write(f'\n{self.summary_prompt}')
        print(f"이야기가 {txt_path}에 저장되었습니다.")

    def _save_image(self, save_dir: str) -> None:
        now = datetime.now()
        img_path = os.path.join(save_dir, f'{now.strftime("%Y%m%d_%H%M%S")}.jpg')
        with open(img_path, 'wb') as file:
            file.write(self.img.content)
        print(f"이미지가 {img_path}에 저장되었습니다.")

    def _save_log(self):
        self.log_data["api_calls"] = get_api_call_logs()
        log_path = os.path.join(self._create_save_directory(), "game_log.json")
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.log_data, f, ensure_ascii=False, indent=2)
        print(f"로그가 {log_path}에 저장되었습니다.")