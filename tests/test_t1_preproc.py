from pathlib import Path
from click.testing import CliRunner
from arcana.core.cli.deploy import make_app
from arcana.core.utils.misc import show_cli_trace

PKG_PATH = Path(__file__).parent.parent.absolute()

runner = CliRunner()

results = runner.invoke(
    make_app,
    [
        f"{PKG_PATH}/specs/australian-imaging-service-community/au/edu/sydney/sydneyimaging",
        "xnat:XnatApp",
        "--raise-errors",
        "--clean-up",
        "--push",
        "--loglevel",
        "info",
        "--use-local-packages",
        "--raise-errors",
        "--use-test-config",
        "--dont-check-registry",
    ],
    catch_exceptions=False,
)

if results.return_value == 0:
    print("Build t1 preproc pipeline successfully")
else:
    print(show_cli_trace(results))