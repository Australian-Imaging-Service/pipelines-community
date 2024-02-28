import os
import logging
import sys
from tempfile import mkdtemp
from unittest.mock import patch
import json
import tempfile
from datetime import datetime
from pathlib import Path
from warnings import warn
import pytest
import requests
import numpy
import docker
import random
import nibabel
from click.testing import CliRunner
from imageio.core.fetching import get_remote_file
import xnat4tests
import medimages4tests.dummy.nifti
import medimages4tests.dummy.dicom.mri.fmap.siemens.skyra.syngo_d13c
from arcana.core.deploy.image.base import BaseImage
from arcana.common import Clinical
from arcana.core.data.set import Dataset
from fileformats.medimage import NiftiGzX, NiftiGz, DicomSeries, NiftiX
from fileformats.text import Plain as Text
from fileformats.image import Png
from fileformats.application import Json
from fileformats.generic import Directory
from arcana.xnat.data.api import Xnat
from arcana.xnat.utils.testing import (
    TestXnatDatasetBlueprint,
    FileSetEntryBlueprint as FileBP,
    ScanBlueprint as ScanBP,
)
from arcana.xnat.data.cs import XnatViaCS

try:
    from pydra import set_input_validator
except ImportError:
    pass
else:
    set_input_validator(True)

# For debugging in IDE's don't catch raised exceptions and let the IDE
# break at it
if os.getenv("_PYTEST_RAISE", "0") != "0":

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call):
        raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo):
        raise excinfo.value

    CATCH_CLI_EXCEPTIONS = False
else:
    CATCH_CLI_EXCEPTIONS = True


@pytest.fixture
def catch_cli_exceptions():
    return CATCH_CLI_EXCEPTIONS


PKG_DIR = Path(__file__).parent


log_level = logging.WARNING

logger = logging.getLogger("arcana")
logger.setLevel(log_level)

sch = logging.StreamHandler()
sch.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sch.setFormatter(formatter)
logger.addHandler(sch)

logger = logging.getLogger("arcana")
logger.setLevel(log_level)

sch = logging.StreamHandler()
sch.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sch.setFormatter(formatter)
logger.addHandler(sch)


@pytest.fixture(scope="session")
def run_prefix():
    "A datetime string used to avoid stale data left over from previous tests"
    return datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")


@pytest.fixture
def cli_runner(catch_cli_exceptions):
    def invoke(*args, catch_exceptions=catch_cli_exceptions, **kwargs):
        runner = CliRunner()
        result = runner.invoke(*args, catch_exceptions=catch_exceptions, **kwargs)
        return result

    return invoke


@pytest.fixture
def work_dir() -> Path:
    work_dir = tempfile.mkdtemp()
    return Path(work_dir)


@pytest.fixture(scope="session")
def build_cache_dir():
    return Path(mkdtemp())


@pytest.fixture(scope="session")
def pkg_dir():
    return PKG_DIR


def access_dataset(
    project_id: str,
    access_method: str,
    xnat_repository: Xnat,
    xnat_archive_dir: Path,
) -> Dataset:
    if access_method == "cs":
        proj_dir = xnat_archive_dir / project_id / "arc001"
        store = XnatViaCS(
            server=xnat_repository.server,
            user=xnat_repository.user,
            password=xnat_repository.password,
            cache_dir=xnat_repository.cache_dir,
            row_frequency=Clinical.dataset,
            input_mount=proj_dir,
            output_mount=Path(mkdtemp()),
        )
    elif access_method == "api":
        store = xnat_repository
    else:
        assert False, f"unrecognised access method {access_method}"
    return store.load_dataset(project_id, name="")


@pytest.fixture(scope="session")
def xnat4tests_config() -> xnat4tests.Config:

    return xnat4tests.Config()


@pytest.fixture(scope="session")
def xnat_root_dir(xnat4tests_config) -> Path:
    return xnat4tests_config.xnat_root_dir


@pytest.fixture(scope="session")
def xnat_archive_dir(xnat_root_dir):
    return xnat_root_dir / "archive"


@pytest.fixture(scope="session")
def xnat_repository(run_prefix, xnat4tests_config):

    xnat4tests.start_xnat()

    repository = Xnat(
        server=xnat4tests_config.xnat_uri,
        user=xnat4tests_config.xnat_user,
        password=xnat4tests_config.xnat_password,
        cache_dir=mkdtemp(),
    )

    # Stash a project prefix in the repository object
    repository.__annotations__["run_prefix"] = run_prefix

    yield repository


@pytest.fixture(scope="session")
def xnat_via_cs_repository(run_prefix, xnat4tests_config):

    xnat4tests.start_xnat()

    repository = Xnat(
        server=xnat4tests_config.xnat_uri,
        user=xnat4tests_config.xnat_user,
        password=xnat4tests_config.xnat_password,
        cache_dir=mkdtemp(),
    )

    # Stash a project prefix in the repository object
    repository.__annotations__["run_prefix"] = run_prefix

    yield repository

