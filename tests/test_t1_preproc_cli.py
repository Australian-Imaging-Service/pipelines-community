from pathlib import Path
from click.testing import CliRunner
from pipeline2app.core.cli import make
from frametree.core.utils import show_cli_trace

PKG_PATH = Path(__file__).parent.parent.absolute()


def test_t1_preproc_pipeline_cli():

    runner = CliRunner()

    results = runner.invoke(
        make,
        [
            f"{PKG_PATH}/specs/australian-imaging-service-community/au/edu/sydney/sydneyimaging",
            "xnat:XnatApp",
            "--raise-errors",
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
