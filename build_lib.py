# Resource = reference to a file which may or may not exist.
# Artifact = a reference to a file created as part of a build command. (probably a subclass of Resource.)
#
# Recipe = (Resource, Resource, List[Dependency]) -> Artifact

import functools
from pathlib import Path

def files_with_suffixes(srcdir, suffixes):
    if type(suffixes) != list:
        suffixes = [suffix]

    files = []
    for suffix in suffixes:
        files += [str(x) for x in Path(srcdir).resolve().glob("**/*" + suffix)]
    return files

class Resource:
    def __init__(self, name):
        self.name = name
        self.deps = set()

    def needs(self, *deps):
        if type(deps) == tuple and len(deps) == 1:
            deps = deps[0]
        self.deps.update(deps)

class Library(Resource):
    def __init__(self, srcdir):
        self.srcdir = srcdir
        super().__init__(srcdir + ".a")

class Executable(Resource):
    pass

# TODO: Implement @recipe() properly.
def recipe(*args, **kwargs):
    def real_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            print(args)
            print(kwargs)
            #print("@recipe({}, {})".format(target, source))
            return function(target, source, deps)
        return wrapper
    return real_decorator

# TODO: Implement build() properly.
def build(resource):
    print("build({})".format(resource))
