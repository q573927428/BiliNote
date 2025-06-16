import os
import glob
from datetime import datetime
from fastapi import APIRouter
from app.utils.qiniu_uploader import upload_to_qiniu

router = APIRouter()

IMG_DIR = 'static/screenshots'
VIDEO_DIR = 'uploads'

def get_files(dir_path: str, extensions: list[str]):
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(dir_path, f'*.{ext}')))
    return files

@router.post("/upload-qiniu")
def upload_files_to_qiniu():
    # 日期路径格式：YYYYMMDD
    date_prefix = datetime.now().strftime("%Y%m%d")

    img_files = get_files(IMG_DIR, ['png', 'jpg', 'jpeg', 'gif'])
    video_files = get_files(VIDEO_DIR, ['mp4', 'mov', 'avi', 'mkv'])

    uploaded = []
    failed = []

    # 上传图片到 YYYYMMDD 目录
    for file_path in img_files:
        filename = os.path.basename(file_path)
        key = f"{date_prefix}/{filename}"  # 七牛云路径
        if upload_to_qiniu(file_path, key):
            uploaded.append(key)
            os.remove(file_path)
        else:
            failed.append(filename)

    # 上传视频到 shipin 目录
    for file_path in video_files:
        filename = os.path.basename(file_path)
        key = f"shipin/{filename}"
        if upload_to_qiniu(file_path, key):
            uploaded.append(key)
            os.remove(file_path)
        else:
            failed.append(filename)

    return {
        "uploaded": uploaded,
        "failed": failed
    }
