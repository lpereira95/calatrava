
import os
import sys
import shutil
from pathlib import Path

GRAPHS_DIR = os.path.join("source", "_graphs")
CONFIGS_DIR = os.path.join("examples", "configs")


def setup(app):

    app.add_config_value(
        'generate_graphs',
        default=True,
        rebuild=False,
    )
    app.add_config_value(
        'examples_dir',
        default="../examples",
        rebuild=False,
    )

    app.connect('builder-inited', startup)
    app.connect('build-finished', cleanup)


def startup(app):
    if not app.builder.config.generate_graphs:
        return

    examples_dir = _get_abspath_from_rel(app.builder.config.examples_dir, app.builder.srcdir)
    sys.path.insert(0, examples_dir)

    cwd = os.getcwd()
    os.chdir(examples_dir)

    from create_graphs import main as create_graphs_
    from create_rst import main as create_rst_

    create_graphs_()
    create_rst_(move=True)

    os.chdir(cwd)


def cleanup(app, exception):
    if not app.builder.config.generate_graphs:
        return

    outdir = app.builder.outdir
    images_dir = os.path.join(outdir, '_images')
    _copy_files(GRAPHS_DIR, images_dir)

    configs_dir = os.path.join(outdir, '_configs')
    os.makedirs(configs_dir, exist_ok=True)
    _copy_files(CONFIGS_DIR, configs_dir)


def _copy_files(source, destination):
    for filename in os.listdir(source):
        new_name = os.path.join(destination, filename)
        if os.path.exists(new_name):
            continue

        previous_name = os.path.join(source, filename)
        shutil.copy(previous_name, new_name)


def _get_abspath_from_rel(relative_path, home):
    rel_path_split = relative_path.split(f'..{os.path.sep}')
    n = len(rel_path_split) - 1
    if n:
        home_ls = home.split(os.path.sep)
        return f'{os.path.sep}'.join(home_ls[:-n] + [rel_path_split[-1]])

    return os.path.join(home, relative_path)