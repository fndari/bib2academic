from pathlib import Path


ADDITIONS = {
    'projects': {
        'my-project-1': ['key1', 'key2'],
        'my-project-2': ['key3', 'key4'],
    },
    'selected': ['key1', 'key3'],
    'updates': {
        'key1': {
            'abstract': 'This is the abstract for the entry `key1`',
        },
        'key2': {
            'abstract': 'And this is the abstract for the entry `key2`',
        }
    }
}

PATH_BASE = Path('/path/to/your/webpage')
PATH_BIB = Path('.')
PATH_OUTPUT = PATH_BASE / 'content/publication'
