# bib2academic

A simple tool to populate the "Publications" section of Hugo websites using the Academic theme using BibTeX files,
written in Python 3.

# Installation

Using virtual environments to manage Python installations is recommended.
However, since this is a simple script requiring no installation, it can be run with the system Python without many issues.
To do so:

1. Clone the repository

```sh
git clone <this-repo-url> <your-installation-path> && cd <your-installation-path>
```

1. Install the dependencies using Pip

- If the default Python version on your system is still Python 2 (check by running `python -V`), the `pip3` command should be used instead of `pip`.
- The `--user` flag tells Pip to install the packages in the Python user directory, as opposed to the Python system directory.

```sh
pip3 install --user requirements.txt
```

# Dependencies

- `bibtexparser` does all the heavy lifting to interact with BibTeX files.
- `invoke` <http://www.pyinvoke.org/> is used to create the command-line interface and run external commands.
    - For more information, read the introduction and the docs at <http://docs.pyinvoke.org/en/latest/>.
- `oyaml` is a drop-in replacement for the `yaml` (PyYAML) module. It's used to keep the same order as the input data in the YAML output.

# Python compatibility

`bib2academic` is compatible with Python 3.5 and up.

# Usage

Beyond the general "populate the 'Publications' section of a Hugo Academic website from BibTeX files", the details of the specific use cases may vary significantly.
For this reason, instead of trying to anticipate all of them and (over-)generalize this script's functionality and API,
I decided to concentrate on my particular workflow, and leave the tool itself as a starting point to be adapted / modified by other users.

In the current incarnation, the tool in structured as follows:

- `bib2academic.py` contains all base functionality and conversion logic
- `tasks.py` is used to define the command-line interface with Invoke
- `settings.py` contains all user-specific settings, including the `ADDITIONS` dictionary used to initialize the corresponding (optional) object storing collective-level updates to each entry.

Once the correct values are defined in `settings.py`, test that everything is working by calling `invoke`/`inv`:

```sh
# list all available Invoke tasks
inv --list
```

If you encounter errors at this point, it could be caused by an incompatible Python executable being used by `invoke` behind-the-scenes.
A quick way to address this is to call `invoke` as a module from a specific Python executable, using the `-m` syntax:

```sh
python3 -m invoke --list
```

Once this works properly, run the desired task, along with any applicable command-line options, e.g.:

```sh
inv process --dry-run
```