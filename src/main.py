import os
from datetime import datetime

import yaml

from crawler.aws_crawler import get_api_data, parse_api_response, insert_to_db


def load_config():
    # 1순위: 환경변수에서 프로젝트 루트 경로 가져오기
    project_root = os.getenv("PROJECT_DIR")

    if not project_root:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

    config_path = os.path.join(project_root, "config/config.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"[ERROR] config.yaml not found at {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # 환경변수에서 ssh_private_key 추가 (없으면 None)
    # 환경변수로 로컬/서버 환경 구분
    # 환경변수가 없으면 기본값은 local
    env = os.getenv("ENVIRONMENT", "local")

    if env == "prod":
        config["ssh"]["ssh_private_key"] = os.getenv("SSH_PRIVATE_KEY")
    else:  # local 환경
        config["ssh"]["ssh_private_key"] = config["ssh"]["ssh_private_key"]

    return config

def process_data(config: dict):
    """API 호출 및 DB 적재를 처리하는 함수"""
    try:
        print(f"[{datetime.now()}] API 호출 및 DB 적재 실행")
        
        # 환경에 따른 SSH 키 경로 설정
        env = os.getenv("ENVIRONMENT", "local")
        if env == "prod":
            pem_temp_path = "/tmp/icuh.pem"
        else:
            pem_temp_path = config["ssh"]["ssh_private_key"]
            if not pem_temp_path:
                raise ValueError("로컬 환경에서는 SSH_PRIVATE_KEY 환경변수 또는 config.yaml에 ssh_private_key가 필요합니다.")
        
        os.chmod(pem_temp_path, 0o600)
        
        response = get_api_data(
            url=config['api']['url'],
            params=config['api']['params'],
            headers=config['api']['headers']
        )
        df = parse_api_response(response)

        if not df.empty:
            insert_to_db(df, db_config=config['database'], ssh_config=config['ssh'])
            print(f"[{datetime.now()}] 데이터 저장 완료")
        else:
            print(f"[{datetime.now()}] 데이터 없음")

    except Exception as e:
        print(f"[{datetime.now()}] 오류 발생: {e}")

def main():
    config = load_config()
    process_data(config)


if __name__ == "__main__":
    print(f"[{datetime.now()}] DB 적재")
    main()
