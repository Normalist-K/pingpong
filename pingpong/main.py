import argparse

from game import StoryGame
from agents import ChatBotAgent, HumanUser


def parse_arguments():
    parser = argparse.ArgumentParser(description="StoryGame Configuration")

    # 참가자 관련 인자
    parser.add_argument("--num_human", type=int, default=1, help="Number of human participants")
    parser.add_argument("--num_chatbot", type=int, default=1, help="Number of chatbot participants")
    
    # StoryGame 관련 인자
    parser.add_argument("--max_turns", type=int, default=4, help="Maximum number of turns")
    parser.add_argument("--termination_msg", type=str, default="The End", help="Termination message")
    parser.add_argument("--keyword", type=str, default="Coca-Cola", help="Keyword for theme generation")
    parser.add_argument("--writing_style", type=str, default="", help="Writing style for the agent")
    parser.add_argument("--gen_img", action='store_true', help="Whether to save the generated image")

    return parser.parse_args()

# python pingpong/main.py --num_human 0 --num_chatbot 6 --max_turns 6 --keyword "라면" --writing_style "유머러스한" --gen_img
def main():
    # 인자 파싱
    args = parse_arguments()

    # 참가자 설정
    participants = []

    # 유저 참가자 추가
    for i in range(args.num_human):
        name = f"Player{i+1}"
        participants.append(HumanUser(name=name))

    # 챗봇 참가자 추가
    for i in range(args.num_chatbot):
        participants.append(ChatBotAgent())

    # 게임 인스턴스 생성 및 실행
    game = StoryGame(participants=participants, max_turns=args.max_turns, termination_msg=args.termination_msg, gen_img=args.gen_img)
    game.start_game(keyword=args.keyword)

if __name__ == "__main__":
    main() 