from pathlib import Path
import pytest
import yaml
from arcana.xnat.deploy.image import XnatApp
from arcana.xnat.deploy.command import XnatCommand
from arcana.xnat.utils.testing import (
    install_and_launch_xnat_cs_command,
)
from fileformats.medimage import NiftiGzX, NiftiGzXBvec


SPECS_DIR = Path(__file__).parent / "specs"


def escape_path(path: Path) -> str:
    return str(path.relative_to(SPECS_DIR)).replace("/", "__")[:-5].replace("-", "_")


def unescape_path(test_name: str) -> Path:
    return SPECS_DIR.joinpath(*test_name.split("__")).with_suffix(".yaml")


@pytest.fixture(
    params=[escape_path(p) for p in (SPECS_DIR).glob("**/*.yaml")]
)
def task_spec_file(request):
    return SPECS_DIR.joinpath(*request.param.split("__")).with_suffix(".yaml")


def test_pipeline(xnat_via_cs_repository, task_spec_file, run_prefix, work_dir):
    """Tests the complete XNAT deployment pipeline by building and running a
    container"""

    with open(task_spec_file) as f:
        build_spec = yaml.safe_load(f)

    # Append run_prefix to command name to avoid clash with previous test runs
    build_spec["name"] = "pipeline" + unescape_path(task_spec_file) + run_prefix

    image_spec = XnatApp(**build_spec)

    image_spec.make(
        build_dir=work_dir,
        arcana_install_extras=["test"],
        use_local_packages=True,
        use_test_config=True,
    )

    # We manually set the command in the test XNAT instance as commands are
    # loaded from images when they are pulled from a registry and we use
    # the fact that the container service test XNAT instance shares the
    # outer Docker socket. Since we build the pipeline image with the same
    # socket there is no need to pull it.
    xnat_command = image_spec.command.make_json()

    launch_inputs = {}

    for inpt, scan in zip(xnat_command["inputs"], blueprint.scans):
        launch_inputs[XnatCommand.path2xnatname(inpt["name"])] = scan.name

    for pname, pval in params.items():
        launch_inputs[pname] = pval

    with xnat_via_cs_repository.connection:

        xlogin = xnat_via_cs_repository.connection

        test_xsession = next(iter(xlogin.projects[dataset.id].experiments.values()))

        workflow_id, status, out_str = install_and_launch_xnat_cs_command(
            command_json=xnat_command,
            project_id=dataset.id,
            session_id=test_xsession.id,
            inputs=launch_inputs,
            xlogin=xlogin,
        )

        assert status == "Complete", f"Workflow {workflow_id} failed.\n{out_str}"

        for deriv in blueprint.derivatives:
            assert [Path(f).name for f in test_xsession.resources[deriv.path].files] == deriv.filenames
