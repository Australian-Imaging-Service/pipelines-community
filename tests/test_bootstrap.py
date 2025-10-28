from pathlib import Path
from click.testing import CliRunner
from pydra2app.core.cli import bootstrap
from frametree.core.utils import show_cli_trace

PKG_PATH = Path(__file__).parent.parent.absolute()

runner = CliRunner()


result = runner.invoke(
    bootstrap,
    [
        "./specs/australian-imaging-service-community/au/edu/${INSTITUTION_NAME}/${GROUP_NAME}/mri_synthstrip.yaml",
        "--author",
        "${AUTHORS_NAME}",
        "${AUTHORS_EMAIL}",
        "--version",
        "1.6",
        "--title",
        "MRI Synthstrip",
        "--base-image",
        "name",
        "freesurfer/synthstrip",
        "--base-image",
        "tag",
        "1.6",
        "--base-image",
        "package_manager",
        "apt",
        "--base-image",
        "python",
        "python3",
        "--packages-system",
        "python3-pip",
        "--docs-url",
        "https://surfer.nmr.mgh.harvard.edu/docs/synthstrip/",
        "--description",
        "'SynthStrip is a skull-stripping tool that extracts brain voxels from a landscape of image types, ranging across imaging modalities, resolutions, and subject populations. It leverages a deep learning strategy to synthesize arbitrary training images from segmentation maps, yielding a robust model agnostic to acquisition specifics.'",
    ],
    catch_exceptions=False,
)

assert not result.exit_code, show_cli_trace(result)
