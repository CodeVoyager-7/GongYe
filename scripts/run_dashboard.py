from pathlib import Path
import subprocess
import sys
import os


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    app_path = project_root / "src" / "app" / "main.py"
    streamlit_home = project_root / ".streamlit-home"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root) + os.pathsep + env.get("PYTHONPATH", "")
    env["HOME"] = str(streamlit_home)
    env["USERPROFILE"] = str(streamlit_home)
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        "8501",
        "--server.address",
        "127.0.0.1",
        "--server.fileWatcherType",
        "none",
    ]
    subprocess.run(cmd, cwd=project_root, env=env, check=True)


if __name__ == "__main__":
    main()
