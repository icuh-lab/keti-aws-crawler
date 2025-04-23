#!/bin/bash

# === 경로 설정 ===
export PROJECT_DIR="/home/ubuntu/keti-aws-crawler"

ENV_NAME="keti_aws_crawler"
LOG_FILE="/home/ubuntu/keti-aws-crawler/logs"
ENV_YML="$PROJECT_DIR/keti_aws_crawler_environment.yml"
CONFIG_PATH="$PROJECT_DIR/config/config.yaml"

# === 로그 시작 ===
mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date)] 스크립트 실행 시작" >> "$LOG_FILE"

# === Conda 초기화 ===
source ~/anaconda3/etc/profile.d/conda.sh

# === Conda 환경 생성 또는 업데이트 ===
if conda env list | grep -q "$ENV_NAME"; then
  echo "[$(date)] Conda 환경 '$ENV_NAME' 존재 - 업데이트 수행" >> "$LOG_FILE"
  conda env update -n "$ENV_NAME" -f "$ENV_YML" >> "$LOG_FILE" 2>&1
else
  echo "[$(date)] Conda 환경 '$ENV_NAME' 없음 - 새로 생성" >> "$LOG_FILE"
  conda env create -n "$ENV_NAME" -f "$ENV_YML" >> "$LOG_FILE" 2>&1
fi

# === config.yaml 생성 여부 확인===
if [ ! -f "$CONFIG_PATH" ]; then
  echo "[$(date)] ERROR: config.yaml 파일이 없습니다. 수동으로 생성해 주세요." >> "$LOG_FILE"
  exit 1
fi

# === Conda 환경 활성화 ===
conda activate "$ENV_NAME"

# === 파이썬 스크립트 실행 ===
cd "$PROJECT_DIR"
python src/main.py >> "$LOG_FILE" 2>&1

# === 로그 종료 ===
echo "[$(date)] 스크립트 실행 완료" >> "$LOG_FILE"
