from pathlib import Path
from click.testing import CliRunner
from pydra2app.core.cli import make
from frametree.core.utils import show_cli_trace

PKG_PATH = Path(__file__).parent.parent.absolute()

runner = CliRunner()

results = runner.invoke(
    make,
    [
        f"{PKG_PATH}/australian-imaging-service-community/",
        "xnat:XnatApp",
        "--raise-errors",
        "--clean-up",
        "--push",
        "--loglevel",
        "info",
    ],
    catch_exceptions=False,
)

print(show_cli_trace(results))
