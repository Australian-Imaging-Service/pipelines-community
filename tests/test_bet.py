from pathlib import Path
import tempfile
from frametree.common import Clinical
from fileformats.medimage import NiftiGz
from frametree.common import FileSystem
from frametree.testing.blueprint import (
    TestDatasetBlueprint,
    FileSetEntryBlueprint as FileBP,
)
from pipeline2app.core import ContainerCommand
from medimages4tests.mri.neuro.t1w import get_image


def test_bet():

    tmp_dir = Path(tempfile.mkdtemp())

    source_dir = tmp_dir / "source"
    source_dir.mkdir()

    NiftiGz(get_image()).copy(source_dir, new_stem="t1w")

    bp = TestDatasetBlueprint(
        hierarchy=["session"],
        axes=Clinical,
        dim_lengths=[1, 1, 1],
        entries=[
            FileBP(path="t1_weighted", datatype=NiftiGz, filenames=["t1w.nii.gz"]),
        ],
    )

    work_dir = Path(tempfile.mkdtemp())

    dataset_id = work_dir / "saved-dataset"
    saved_dataset = bp.make_dataset(
        FileSystem(), dataset_id, name="", source_data=source_dir
    )

    command_spec = ContainerCommand(
        task="common:shell",
        row_frequency=Clinical.session,
        inputs=[
            {
                "name": "t1w",
                "datatype": "medimage/nifti-gz",
                "help": "T1-weighted image",
                "configuration": {
                    "argstr": "",
                    "position": -2,
                },
            },
        ],
        outputs=[
            {
                "name": "brain",
                "datatype": "medimage/nifti-gz",
                "help": "dummy",
                "configuration": {
                    "argstr": "",
                    "position": -1,
                },
            }
        ],
        configuration={
            "executable": "bet",
        },
    )
    # Start generating the arguments for the CLI
    # Add source to loaded dataset
    command_spec.execute(
        dataset_locator=saved_dataset.locator,
        input_values=[
            ("t1w", "t1_weighted"),
        ],
        output_values=[
            ("brain", "extracted_brain"),
        ],
        raise_errors=True,
        plugin="serial",
        work_dir=str(work_dir),
        loglevel="info",
        dataset_hierarchy=["session"],
        pipeline_name="bet_pipeline",
    )
    # Add source column to saved dataset
    sink = saved_dataset.add_sink("extracted_brain", NiftiGz)
    brain = next(iter(sink))
    print(f"Zipped directory at {brain}")
