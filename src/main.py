from datetime import datetime

from utils.helpers import load_config
from crawler.aws_crawler import get_api_data, parse_api_response, insert_to_db

def main():
    config = load_config()

    try:
        print(f"[{datetime.now()}] API 호출 및 DB 적재 실행")
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

if __name__ == "__main__":
    print(f"[{datetime.now()}] 스케줄러 시작")
    main()
