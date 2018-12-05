import bibtexparser
from bibtexparser.latexenc import latex_to_unicode

from pathlib import Path
from collections import OrderedDict
import oyaml as yaml


def is_conference(journal):
    jn = journal.lower()
    return 'conf' in jn or jn in ['pos']


def to_single_line(s):
    return s.replace('\n', ' ')


def remove_enclosing_braces(s):
    # this is of course very rudimentary
    if s.startswith('{') and s.endswith('}'):
        return s[1:-1]
    return s


def process(obj, ops):
    """
    Process `obj` with a sequence of operations (unary callables).
    """
    for op in ops:
        obj = op(obj)
    return obj


def get_dummy_date(year):
    return '{year}-01-01'.format(**locals())


class Additions:

    def __init__(self, src):
        self._src = src

    @property
    def updates(self):
        return self._src.get('updates', {})

    @property
    def projects(self):
        return self._src.get('projects', {})

    @property
    def selected(self):
        return self._src.get('selected', [])

    def get_updates(self, key):
        return self.updates.get(key, {})


class AcademicPub:

    @classmethod
    def from_path(cls, path, **kwargs):
        path = Path(path)
        with path.open() as f:
            bib_db = bibtexparser.load(f)

        return [cls(entry, path_bib=path, **kwargs) for entry in bib_db.entries]

    def __init__(self, bib, additions=None, path_bib=None):
        self.bib = bib
        self.additions = additions
        # in case it's needed for some logic
        self.path_bib = path_bib
        
    @property
    def id(self):
        return self.bib['ID']
    
    @property
    def authors(self):
        auth = process(self.bib['author'], [to_single_line, remove_enclosing_braces, latex_to_unicode])

        coll = self.bib.get('collaboration')
        if coll:
            auth = '{auth} ({coll})'.format(**locals())

        return [auth]  # Academic wants a list of authors
    
    @property
    def title(self):
        return process(self.bib['title'], [to_single_line, remove_enclosing_braces])
    
    @property
    def doi(self):
        return self.bib.get('doi', '')
    
    @property
    def keywords(self):
        # the bib field is "keyword", not "keywords"
        return self.bib.get('keyword', [])
    
    @property
    def publication_types(self):
        types = []
        if self.bib['ENTRYTYPE'] == 'article':
            types.append('1')
        if is_conference(self.bib['journal']):
            types.append('2')
        
        return types
    
    @property
    def selected(self):
        return 'selected' in self.keywords
    
    def get_list_from_bib_val(self, raw, sep=','):
        if not raw:
            return []  # otherwise it would return [''], which is true-y synctactically, but not semantically
        return [item.strip() for item in raw.split(sep)]
    
    @property
    def tags(self):
        return self.get_list_from_bib_val(self.bib.get('hugotags', ''))
    
    @property
    def projects(self):
        return self.get_list_from_bib_val(self.bib.get('hugoprojects', ''))

    @property
    def publication(self):
        jn = self.bib['journal']
        vol = self.bib['volume']
        return 'In: *{jn}* {vol}'.format(**locals())
    
    @property
    def publication_short(self):
        return self.publication

    @property
    def date(self):
        return get_dummy_date(self.bib['year'])

    @property
    def math(self):
        return True
    
    @property
    def name(self):
        return self.bib.get('hugoname', self.fallback_name)
    
    @property
    def fallback_name(self):
        # TODO this should be a real slugifier
        def slugify(s):
            return s.lower().replace(':', '-')
    
        return slugify(self.bib['ID'])

    fields_frontmatter = ['id', 'title', 'date', 'authors', 'doi', 'publication', 'publication_types', 'selected', 'tags', 'projects', 'math']
    
    def to_dict(self):
        # first layer, using the information from the bib entry
        d = OrderedDict([(key, getattr(self, key)) for key in self.fields_frontmatter])

        if self.additions:
            d.update(self.get_updates(self.additions))
        
        return d

    def get_updates(self, adds):
        updates = {}
        # second layer, which we could call "slice_update" or sth
        projects_bib = self.projects
        for project, ids in adds.projects.items():
            # genuinely terrible
            if self.id in ids and project not in projects_bib:
                updates['projects'] = [project] + projects_bib
        if self.id in adds.selected:
            updates['selected'] = True
       
        # third layer
        updates.update(adds.get_updates(self.id))

        return updates

    def to_yaml(self):
        data = self.to_dict()

        return yaml.dump(data, allow_unicode=True)
    
    def get_frontmatter(self, fmt='yaml', sep=None):
        if fmt.startswith('y'):
            sep = '---'
            f = self.to_yaml

        return sep + '\n' + f() + '\n' + sep

    def to_hugo(self, path=None, path_base=None, name=None, suffix='.md'):

        if path is None:
            if path_base is not None:
                name = name or self.name
                path = (Path(path_base) / name).with_suffix(suffix)
        
        text = self.get_frontmatter()
        
        if path:
            with Path(path).open('w') as f:
                f.write(text)
        else:
            print(text)
