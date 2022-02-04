from pathlib import Path
from pydra import mark
from arcana.data.types.general import text


@mark.task
def concatenate(in_file1: Path, in_file2: Path, out_file: Path=None,
                duplicates: int=1) -> Path:
    """Concatenates the contents of two files and writes them to a third

    Parameters
    ----------
    in_file1 : Path
        A text file
    in_file2 : Path
        Another text file
    out_file : Path
       The path to write the output file to 

    Returns
    -------
    Path
        A text file made by concatenating the two inputs
    """
    if out_file is None:
        out_file = Path('out_file.txt').absolute()
    contents = []
    for _ in range(duplicates):
        for fname in (in_file1, in_file2):
            with open(fname) as f:
                contents.append(f.read())
    with open(out_file, 'w') as f:
        f.write('\n'.join(contents))
    return out_file


spec = {
    'package_name': "demo",
    'description': (
        "A demonstraction package to be used as a template for defining new "
        "wrapper specificiations"),
    'commands': [
        {'pydra_task': __name__ + ':task',  # Path to the pydra task interface
         'inputs': [('in_file1', text), ('in_file2', text)],
         'outputs': [('out', text)],
         'parameters': ['duplicates']}],
    'version': 1,
    'pkg_version': 1.0,
    'packages': [],
    'python_packages': [],
    'base_image': 'debian:buster-slim',
    'maintainer': 'thomas.close@sydney.edu.au',
    'info_url': 'http://concatenate-docs.at.some.url'}
