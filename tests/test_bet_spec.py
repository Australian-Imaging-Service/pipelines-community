from pathlib import Path
from click.testing import CliRunner
from pydra2app.core.cli import make
from frametree.core.utils import show_cli_trace

PKG_PATH = Path(__file__).parent.parent.absolute()

runner = CliRunner()


result = runner.invoke(
    make,
    [
        "xnat",
        "/Users/tclo7153/git/workflows/pipelines-community/specs/australian-imaging-service-community/examples/bet.yaml",
        "--spec-root",
        "/Users/tclo7153/git/workflows/pipelines-community/specs",
        "--for-localhost",
        "--export-file",
        "xnat_command.json",
        "/Users/tclo7153/bet-xnat-command.json",
    ],
    catch_exceptions=False,
)

assert not result.exit_code, show_cli_trace(result)
