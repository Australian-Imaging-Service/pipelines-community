from pathlib import Path
from click.testing import CliRunner
from arcana.core.cli.deploy import make_app
from arcana.core.utils.misc import show_cli_trace

PKG_PATH = Path(__file__).parent.parent.absolute()

runner = CliRunner()

results = runner.invoke(
    make_app,
    [
        f"{PKG_PATH}/australian-imaging-service-community/",
        "xnat:XnatApp",
        "--raise-errors",
        "--clean-up",
        "--loglevel",
        "info",
    ],
    catch_exceptions=False,
)

print(show_cli_trace(results))
