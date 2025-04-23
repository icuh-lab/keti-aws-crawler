from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder

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
