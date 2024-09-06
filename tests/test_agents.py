# tests/test_agents.py
import pytest
from pingpong.agents import ThemeSelectionAgent, ChatBotAgent

def test_theme_selection_agent():
    agent = ThemeSelectionAgent()
    theme = agent.generate_theme("magic")
    assert "magic" in theme

def test_chat_bot_agent():
    agent = ChatBotAgent()
    sentence = agent.generate_sentence("magic", [])
    assert isinstance(sentence, str)