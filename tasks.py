from invoke import task
from pathlib import Path

from bib2academic import AcademicPub, Additions
from settings import *

@task
def list_bib(c, bib_path=PATH_BIB):
    """
    List BibTeX files in `bib_path`.
    """
    files = Path(bib_path).glob('*.bib')
    print(list(files))


@task
def process(c, filename, output_path=PATH_OUTPUT, bib_path=PATH_BIB, open_output_dir=False, dry_run=False):
    """
    Process entries in BibTeX file `filename`, and generate Hugo markdown files in `output_path`.
    """
    output_path = Path(output_path)
    output_path.mkdir(exist_ok=True)

    for pub in AcademicPub.from_path(bib_path / filename, additions=Additions(ADDITIONS)):
        pub.to_hugo(path_base=(None if dry_run else output_path))
    
    if open_output_dir:
        c.run('xdg-open {} &'.format(output_path))
