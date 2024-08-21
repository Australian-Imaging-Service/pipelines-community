from pathlib import Path
import tempfile
import operator as op
import functools
from fileformats.generic import Directory
from fileformats.application import Zip
from frametree.common import FileSystem
from frametree.testing import TestAxes
from frametree.testing.blueprint import (
    TestDatasetBlueprint,
    FileSetEntryBlueprint as FileBP,
)
from pydra2app.core.command import ContainerCommand


bp = TestDatasetBlueprint(
    hierarchy=[
        "abcd"
    ],  # e.g. XNAT where session ID is unique in project but final layer is organised by timepoint
    space=TestAxes,
    dim_lengths=[1, 1, 1, 1],
    entries=[
        FileBP(path="dir1", datatype=Directory, filenames=["dir"]),
    ],
)

work_dir = Path(tempfile.mkdtemp())

dataset_id = work_dir / "saved-dataset"
saved_dataset = bp.make_dataset(FileSystem(), dataset_id, name="")

command_spec = ContainerCommand(
    task="arcana.common:shell",
    row_frequency=bp.space.default(),
    inputs=[
        {
            "name": "to_zip",
            "datatype": "generic/directory",
            "help": "directory to zip",
            "configuration": {
                "argstr": "",
                "position": -1,
            },
        },
    ],
    outputs=[
        {
            "name": "zipped",
            "datatype": "application/zip",
            "help": "dummy",
            "configuration": {
                "argstr": "",
                "position": -2,
            },
        }
    ],
    parameters=[
        {
            "name": "compression",
            "datatype": "int",
            "help": "the level of compression applied",
            "default": 5,
            "configuration": {
                "argstr": "-{compression}",
            },
        }
    ],
    configuration={
        "executable": "zip",
    },
)
# Start generating the arguments for the CLI
# Add source to loaded dataset
command_spec.execute(
    dataset_locator=saved_dataset.locator,
    input_values=[
        ("to_zip", "dir1"),
    ],
    output_values=[
        ("zipped", "zipped_dir"),
    ],
    raise_errors=True,
    plugin="serial",
    work_dir=str(work_dir),
    loglevel="info",
    dataset_hierarchy=",".join(bp.hierarchy),
    pipeline_name="zip_pipeline",
)
# Add source column to saved dataset
sink = saved_dataset.add_sink("zipped_dir", Zip[Directory])
zipped = next(iter(sink))
print(f"Zipped directory at {zipped}")
