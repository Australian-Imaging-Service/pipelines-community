import sys
from click.testing import CliRunner
from pipeline2app.core.cli import make_docs

runner = CliRunner()
runner.invoke(make_docs, args=sys.argv[1:], catch_exceptions=False)
