import json
import logging
import requests
import streamlit as st
from datetime import datetime

def get_gist_content(gist_id):
    """GitHub Gist에서 데이터 읽기"""
    try:
        gist_token = st.secrets["github"]["gist_token"]
        headers = {
            'Authorization': f'token {gist_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(
            f'https://api.github.com/gists/{gist_id}',
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching gist {gist_id}: {str(e)}")
        raise

def update_gist(gist_id, files):
    """GitHub Gist 업데이트"""
    try:
        gist_token = st.secrets["github"]["gist_token"]
        headers = {
            'Authorization': f'token {gist_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            "files": files
        }
        
        response = requests.patch(
            f'https://api.github.com/gists/{gist_id}',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error updating gist {gist_id}: {str(e)}")
        raise

def load_rooms():
    """채팅방 데이터를 Gist에서 읽어옴"""
    try:
        gist_id = st.secrets["github"]["rooms_gist_id"]
        gist = get_gist_content(gist_id)
        content = gist['files']['rooms.json']['content']
        return json.loads(content)
    except Exception as e:
        logging.error(f"Error loading rooms: {str(e)}")
        return []

def save_rooms(rooms):
    """채팅방 데이터를 Gist에 저장"""
    try:
        gist_id = st.secrets["github"]["rooms_gist_id"]
        files = {
            "rooms.json": {
                "content": json.dumps(rooms, indent=2)
            }
        }
        update_gist(gist_id, files)
        logging.info("Rooms data saved to Gist")
    except Exception as e:
        logging.error(f"Error saving rooms: {str(e)}")
        raise

def load_messages(room_id):
    """특정 채팅방의 메시지를 Gist에서 읽어옴"""
    try:
        gist_id = st.secrets["github"]["messages_gist_id"]
        gist = get_gist_content(gist_id)
        filename = f"messages_{room_id}.json"
        
        if filename in gist['files']:
            content = gist['files'][filename]['content']
            return json.loads(content)
        return []
    except Exception as e:
        logging.error(f"Error loading messages for room {room_id}: {str(e)}")
        return []

def save_messages(room_id, messages):
    """특정 채팅방의 메시지를 Gist에 저장"""
    try:
        gist_id = st.secrets["github"]["messages_gist_id"]
        gist = get_gist_content(gist_id)
        
        # 기존 메시지들 유지
        files = {
            name: {"content": file["content"]} 
            for name, file in gist['files'].items()
        }
        
        # 새로운/수정된 메시지 추가
        files[f"messages_{room_id}.json"] = {
            "content": json.dumps(messages, indent=2)
        }
        
        update_gist(gist_id, files)
        logging.info(f"Messages saved for room {room_id}")
    except Exception as e:
        logging.error(f"Error saving messages: {str(e)}")
        raise

def delete_room(room_id):
    """채팅방 삭제 및 백업"""
    try:
        # 채팅방 정보 백업
        rooms = load_rooms()
        deleted_room = next((room for room in rooms if room['id'] == room_id), None)
        
        if deleted_room:
            # 삭제 시간 추가
            deleted_room['deleted_at'] = datetime.now().isoformat()
            
            # 백업 Gist에 저장
            backup_gist_id = st.secrets["github"]["backup_gist_id"]
            gist = get_gist_content(backup_gist_id)
            
            # 기존 백업 유지
            files = {
                name: {"content": file["content"]} 
                for name, file in gist['files'].items()
            }
            
            # 새로운 백업 추가
            backup_time = deleted_room['deleted_at'].replace(":", "-")
            files[f"room_{room_id}_{backup_time}.json"] = {
                "content": json.dumps(deleted_room, indent=2)
            }
            
            # 메시지도 백업
            messages = load_messages(room_id)
            files[f"messages_{room_id}_{backup_time}.json"] = {
                "content": json.dumps(messages, indent=2)
            }
            
            update_gist(backup_gist_id, files)
            
            # rooms.json에서 해당 방 제거
            rooms = [room for room in rooms if room['id'] != room_id]
            save_rooms(rooms)
            
            logging.info(f"Room {room_id} deleted and backed up to Gist")
            return True
            
    except Exception as e:
        logging.error(f"Error deleting room {room_id}: {str(e)}")
        raise