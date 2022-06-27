

import click


from calatrava.filters import load_filters_from_json
from calatrava.graphviz.uml import (
    create_graph,
    save_graph,
    Package,
    PackageManager,
)


def _handle_variadic_input(args):
    packages = []
    imports = []

    for arg in args:
        if len(arg.split('.')) > 1:
            imports.append(arg)
        else:
            packages.append(arg)

    return packages, imports


@click.group()
def main_cli():
    pass


@click.command()
@click.argument("args", nargs=-1, type=str, required=True)
@click.option("--output-filename", "-o", type=str,
              default="calatrava_tree")
@click.option("--output-format", type=str, default='svg')
@click.option("--filters-filename", '-f', type=str, default='')
def uml(args, output_filename, output_format, filters_filename):
    """Builds UML diagram.
    """
    packages_paths, imports = _handle_variadic_input(args)

    packages = [Package(package_path) for package_path in packages_paths]
    package_manager = PackageManager(packages)

    if imports:
        for import_ in imports:
            package_manager.find(import_)
    else:
        package_manager.find_all()

    package_manager.update_inheritance()

    classes = list(package_manager.get_classes().values())

    if filters_filename:
        filters = load_filters_from_json(filters_filename) if filters_filename else []

    dot = create_graph(classes, filters=filters)

    save_graph(dot, output_filename, view=True, format=output_format)


main_cli.add_command(uml)
