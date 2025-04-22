# KETI AWS Crawler

## 설정 방법

1. `config/config.yaml.example` 파일을 `config/config.yaml`로 복사합니다:
```bash
cp config/config.yaml.example config/config.yaml
```

2. `config.yaml` 파일을 환경에 맞게 수정합니다:
   - API 설정
   - 데이터베이스 설정
   - SSH 설정

3. 환경변수 설정:
   - `ENVIRONMENT`: 실행 환경 (local/prod)
   - `SSH_PRIVATE_KEY`: SSH 개인키 경로
   - `PROJECT_DIR`: 프로젝트 루트 경로 (선택사항)

## 주의사항
- `config.yaml` 파일은 Git에서 제외되어 있습니다.
- 실제 설정값은 `config.yaml.example`을 참고하여 생성하세요.
- 민감한 정보는 환경변수로 관리하는 것을 권장합니다.