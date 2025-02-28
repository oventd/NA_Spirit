import logging
import os
from datetime import datetime

def get_logger(process_name, log_path=None):
    """각 DB 작업마다 별도 로그 파일을 생성하는 로거 반환"""
    if log_path is None:
        log_file_name = f"{process_name}_{datetime.now().strftime('%Y-%m-%d')}.log"
    else:
        abs_path = os.path.abspath(log_path)

        if os.path.isdir(abs_path):  # 디렉터리인 경우
            log_dir = abs_path
            log_file_name = f"{process_name}_{datetime.now().strftime('%Y-%m-%d')}.log"
        else:  # 파일 경로인 경우
            log_dir = os.path.dirname(abs_path)
            log_file_name = os.path.basename(abs_path)

    os.makedirs(log_dir, exist_ok=True)  # ✅ 디렉터리 존재 확인 후 생성

    log_file_path = os.path.join(log_dir, log_file_name)

    logger = logging.getLogger(process_name)

    if not logger.hasHandlers():  # ✅ 중복 핸들러 방지
        handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    return logger

