# from . backtest import backtest
# from . analyzer import main as run_analyzer

# from .loader import Loader
# from .processor import Processor
# from .database import Database
# from .manager import main as run_analyzer
# from .processor import Processor

""" Analyzer bot """
__version__ = 'develop'
__logger__ = 'analyzer'

if __version__ == 'develop':

    try:
        import subprocess

        __version__ = 'develop-' + subprocess.check_output(
            ['git', 'log', '--format="%h"', '-n 1'],
            stderr=subprocess.DEVNULL).decode("utf-8").rstrip().strip('"')

        # from datetime import datetime
        # last_release = subprocess.check_output(
        #     ['git', 'tag']
        # ).decode('utf-8').split()[-1].split(".")
        # # Releases are in the format "2020.1" - we increment the latest version for dev.
        # prefix = f"{last_release[0]}.{int(last_release[1]) + 1}"
        # dev_version = int(datetime.now().timestamp() // 1000)
        # __version__ = f"{prefix}.dev{dev_version}"

        #  subprocess.check_output(
        #     ['git', 'log', '--format="%h"', '-n 1'],
        #     stderr=subprocess.DEVNULL).decode("utf-8").rstrip().strip('"')
    except Exception:  # pragma: no cover
        # git not available, ignore
        try:
            # Try Fallback to analyzer_commit file (created by CI while building docker image)
            from pathlib import Path
            versionfile = Path('./analyzer_commit')
            if versionfile.is_file():
                __version__ = f"docker-{versionfile.read_text()[:8]}"
        except Exception:
            pass
