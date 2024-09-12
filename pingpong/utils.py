import subprocess

def get_commit_info():
    try:
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        commit_message = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode("utf-8").strip()
        return {"hash": commit_hash, "message": commit_message}
    except subprocess.CalledProcessError:
        return {"error": "Git 정보를 가져오는 데 실패했습니다."}
