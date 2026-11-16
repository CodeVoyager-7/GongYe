import os
import subprocess
import sys


def main() -> None:
    env = os.environ.copy()
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    subprocess.run([sys.executable, "-m", "pytest", "-q"], env=env, check=True)


if __name__ == "__main__":
    main()
