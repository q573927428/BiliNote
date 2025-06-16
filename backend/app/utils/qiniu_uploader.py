import os
from qiniu import Auth, put_file
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("ACCESSKEY")
SECRET_KEY = os.getenv("SECRETKEY")
BUCKET_NAME = os.getenv("BUCKET")

auth = Auth(ACCESS_KEY, SECRET_KEY)

def upload_to_qiniu(file_path: str, key: str) -> bool:
    token = auth.upload_token(BUCKET_NAME, key)
    ret, info = put_file(token, key, file_path)
    return info.status_code == 200
