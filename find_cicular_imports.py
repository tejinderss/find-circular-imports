from collections import defaultdict
from itertools import combinations

import click
from unipath import Path, FILES


@click.command()
@click.argument('path', type=click.Path(
    exists=True, file_okay=False, dir_okay=True, readable=True))
@click.option(
    '--prefix', default='.',
    help='Provides the prefix for the from import statement. '
         'Default is current relative path "."')
def check_circular_imports(path, prefix):
    path = Path(path)
    python_files_paths = path.listdir(filter=FILES, pattern='*.py')
    relative_import_modules = defaultdict(list)
    for pyf in python_files_paths:
        import_pattern = 'from {0} import '.format(prefix)
        with open(pyf, 'r') as f:
            for line in f.read().splitlines():
                if line.startswith(import_pattern):
                    modules_names = line[len(import_pattern):].replace(" ", "").split(',')
                    relative_import_modules[pyf.stem].extend(modules_names)

    for module, next_module in combinations(relative_import_modules.keys(), 2):
        module_modules = relative_import_modules[module]
        next_module_modules = relative_import_modules[next_module]
        if module.name in next_module_modules and next_module.name in module_modules:
            print "Circular imports in modulse {0} and {1}".format(
                module, next_module)


if __name__ == '__main__':
    check_circular_imports()
