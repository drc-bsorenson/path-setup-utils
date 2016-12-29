import os
import yaml
import argparse
import sys


PATH_DFLT_TEMPLATES = os.path.join(os.path.split(os.path.abspath(__file__))[0], '../templates')
PATH_DFLT_TEMPLATES = os.path.abspath(PATH_DFLT_TEMPLATES)


def walk_tree(node, root=None):
    if root is None:
        root = ''
    for branch, children in node.items():
        if branch.strip().endswith(':'):
            branch = os.path.join(branch, os.sep)
        for child in children:
            if child is None:
                continue
            if isinstance(child, dict):
                yield from walk_tree(child, os.path.join(root, branch))
            else:
                yield os.path.join(root, branch, child)


def make_tree(template, **kwargs):
    return yaml.load(template.format(**dict(os.environ, **kwargs)))


def main(template, mapping, template_path=PATH_DFLT_TEMPLATES, dry_run=False):

    if dry_run:
        print('DRY RUN! No, paths will be created.')
    if not os.path.exists(template):
        template = os.path.join(template_path, template)

    template = open(template).read()

    tree = make_tree(template, **dict(mapping))
    for path in walk_tree(tree):
        if os.path.exists(path):
            print('Skipping: "%s" Already Exists' % path)
        else:
            print('Creating: "%s"' % path)
            if not dry_run:
                os.makedirs(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('template', help='Name of template file')
    parser.add_argument('-m', '--mapping', nargs=2, action='append',
                        help='key, value mapping pairs to fill in template')
    parser.add_argument('-d', '--dry-run', dest='dry_run', help=('Print directories that will be created, but'
                                                                 "don't create them"),
                        action='store_true')
    parser.set_defaults(dry_run=False)

    main(**vars(parser.parse_args()))
