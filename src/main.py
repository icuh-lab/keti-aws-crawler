import os
import yaml

from datetime import datetime
from parser.json_timeseries_parser import call_keti_aws_api

def load_config():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    config_path = os.path.join(project_root, "config/config.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"[ERROR] config.yaml not found at {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config

def main():
    config = load_config()
    call_keti_aws_api(config)


if __name__ == "__main__":
    print(f"[{datetime.now()}] KETI-AWS-DB 적재")
    main()
