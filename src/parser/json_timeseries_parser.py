import os
import pandas as pd
import pytz
import requests

from datetime import datetime
from src.utils.insert_db import insert_to_db

# -----------------------------
# 기능 함수
# -----------------------------

# API 호출한 뒤 응답 데이터 받아오기
def get_api_data(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


# 받아온 응답 데이터를 딕셔너리 형태로 포멧
def parse_api_response(response):
    tz = pytz.timezone('Asia/Seoul')
    data = []

    for item in response:
        row = {'aws_stn_id': int(item['id'].split(':')[-1])}
        if 'TA_AVG' in item:
            observed = pd.to_datetime(item['TA_AVG']['observedAt']).astimezone(tz)
            row['DATE'] = observed.strftime('%Y-%m-%d')
            row['TIME'] = observed.strftime('%H:%M')

        for key, val in item.items():
            if key in ['id', 'type', '@context']:
                continue
            row[key] = float(val['value'])

        data.append(row)

    return pd.DataFrame(data)


def call_keti_aws_api(config: dict):
    """API 호출 및 DB 적재를 처리하는 함수"""
    try:
        print(f"[{datetime.now()}] API 호출 및 DB 적재 실행")

        # TODO: load_total_config랑 내용이 겹침
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
