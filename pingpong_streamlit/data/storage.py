import json
import logging
from config.settings import ROOMS_FILE, DATA_DIR
from utils.validators import secure_file_path
import shutil
from datetime import datetime
import requests
import os
import streamlit as st


def load_rooms():
    """채팅방 데이터를 파일에서 읽어옴"""
    try:
        if ROOMS_FILE.exists():
            with open(ROOMS_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logging.error(f"Error loading rooms: {str(e)}")
        return []

def save_rooms(rooms):
    """채팅방 데이터를 파일에 저장"""
    try:
        with open(ROOMS_FILE, 'w') as f:
            json.dump(rooms, f, indent=2)
        logging.info("Rooms data saved successfully")
    except Exception as e:
        logging.error(f"Error saving rooms: {str(e)}")
        raise

def load_messages(room_id):
    """특정 채팅방의 메시지를 파일에서 읽어옴"""
    try:
        file_path = secure_file_path(room_id)
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logging.error(f"Error loading messages for room {room_id}: {str(e)}")
        return []

def save_messages(room_id, messages):
    """특정 채팅방의 메시지를 파일에 저장"""
    try:
        # 로컬 저장
        file_path = secure_file_path(room_id)
        with open(file_path, 'w') as f:
            json.dump(messages, f, indent=2)
            
        # Gist 백업 (클라우드 환경일 때만)
        if os.getenv('STREAMLIT_CLOUD'):
            backup_to_gist(room_id, messages)
            
        logging.info(f"Messages saved for room {room_id}")
    except Exception as e:
        logging.error(f"Error saving messages: {str(e)}")
        raise

def delete_room(room_id):
    """채팅방 삭제"""
    try:
        # 백업 디렉토리 생성
        backup_dir = DATA_DIR / "deleted_rooms"
        backup_dir.mkdir(exist_ok=True)
        
        # 채팅방 정보 백업
        rooms = load_rooms()
        deleted_room = next((room for room in rooms if room['id'] == room_id), None)
        if deleted_room:
            # 삭제 시간 추가
            deleted_room['deleted_at'] = datetime.now().isoformat()
            
            # 백업 파일 생성
            backup_file = backup_dir / f"room_{room_id}_{deleted_room['deleted_at']}.json"
            with open(backup_file, 'w') as f:
                json.dump(deleted_room, f, indent=2)
            
            # 채팅 메시지 백업
            msg_file = secure_file_path(room_id)
            if msg_file.exists():
                backup_msg_file = backup_dir / f"messages_{room_id}_{deleted_room['deleted_at']}.json"
                shutil.copy2(msg_file, backup_msg_file)
                msg_file.unlink()  # 원본 메시지 파일 삭제
            
            # rooms.json에서 해당 방 제거
            rooms = [room for room in rooms if room['id'] != room_id]
            save_rooms(rooms)
            
            logging.info(f"Room {room_id} deleted and backed up")
            return True
            
    except Exception as e:
        logging.error(f"Error deleting room {room_id}: {str(e)}")
        raise

def backup_to_gist(room_id, messages):
    """채팅 기록을 GitHub Gist에 백업"""
    try:
        gist_token = st.secrets["github"]["gist_token"]
        headers = {
            'Authorization': f'token {gist_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            "description": f"Chat backup for room {room_id}",
            "public": False,
            "files": {
                f"chat_{room_id}.json": {
                    "content": json.dumps(messages, indent=2)
                }
            }
        }
        
        response = requests.post(
            'https://api.github.com/gists',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        return response.json()["id"]
        
    except Exception as e:
        logging.error(f"Error backing up to Gist: {str(e)}")
        raise