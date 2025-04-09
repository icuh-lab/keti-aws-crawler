import pandas as pd
import pytz
import requests

from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from datetime import datetime

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


# ssh 연결
def connect_ssh_tunnel(ssh_config):
    tunnel = SSHTunnelForwarder(
        (ssh_config['ssh_host'], ssh_config['ssh_port']),
        ssh_username=ssh_config['ssh_username'],
        ssh_private_key=ssh_config['ssh_private_key'],
        remote_bind_address=(
            ssh_config['remote_bind_address']['host'],
            ssh_config['remote_bind_address']['port']
        ),
        local_bind_address=(
            ssh_config['local_bind_address']['host'],
            ssh_config['local_bind_address']['port']
        )
    )
    tunnel.start()
    return tunnel


def insert_to_db(df, db_config, ssh_config):
    tunnel = connect_ssh_tunnel(ssh_config)
    engine = create_engine(
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@127.0.0.1:{ssh_config['local_bind_address']['port']}/{db_config['name']}"
    )
    df.to_sql(name="KETI_BASE_TB", con=engine, if_exists="append", index=False)
    tunnel.close()


# -----------------------------
# 스케줄러에 등록할 메인 작업
# -----------------------------

def get_data_from_api():
  try:
    print(f"[{datetime.now()}] API 호출 및 DB 적재 실행")
    response = get_api_data()
    df = parse_api_response(response)

    if not df.empty:
      insert_to_db(df)
      print(f"[{datetime.now()}] 데이터 저장 완료")
    else:
      print(f"[{datetime.now()}] 데이터 없음")

  except Exception as e:
    print(f"[{datetime.now()}] 호출하고 저장하는 과정에서 오류 발생: {e}")


def main():
  print(f"[{datetime.now()}] 스케줄러 시작")
  get_data_from_api()

if __name__ == "__main__":
  main()

