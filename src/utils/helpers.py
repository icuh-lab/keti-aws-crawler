import yaml
import os

from dotenv import load_dotenv

def load_env():
    env = os.getenv("ENV", "local")
    dotenv_path = f".env.{env}"
    load_dotenv(dotenv_path=dotenv_path)
    print(f" Loaded environment: {env}")

def load_config():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    config_path = os.path.join(project_root, "config/config.yaml")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # .env에 있는 ssh_private_key 추가
    config["ssh"]["ssh_private_key"] = os.getenv("SSH_PRIVATE_KEY")
    return config
