from pathlib import Path
import sys


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    from src.app.services.auth import ensure_auth_schema, get_auth_config

    cfg = get_auth_config()
    ok, message = ensure_auth_schema(cfg)
    if not ok:
        raise RuntimeError(message)

    print(f"Initialized MySQL auth table: {cfg.host}:{cfg.port}/{cfg.database}.{cfg.table}")
    print(f"Initialized MySQL code table: {cfg.host}:{cfg.port}/{cfg.database}.{cfg.code_table}")
    print("Default platform login: admin / 123456")
    print("Default phone login: 13800000000 / verification code")


if __name__ == "__main__":
    main()
