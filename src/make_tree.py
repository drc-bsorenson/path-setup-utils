import os
import yaml
import argparse
import jinja2 as jj

PATH_DFLT_TEMPLATES = os.path.join(os.path.split(os.path.abspath(__file__))[0], '../templates')
PATH_DFLT_TEMPLATES = os.path.abspath(PATH_DFLT_TEMPLATES)


def walk_tree(node, root=None):
    if root is None:
        root = ''
    for branch, children in node.items():
        if branch.strip().endswith(':'):
            branch = os.path.join(branch, os.sep)
        if children is None:
            yield os.path.join(root, branch)
        else:
            yield from walk_tree(children, os.path.join(root, branch))


def make_tree(template, **kwargs):
    template = jj.Template(template)
    return yaml.load(template.render(**dict(os.environ, **kwargs)))


def main(template, mapping, template_path=PATH_DFLT_TEMPLATES, dry_run=False):

    if dry_run:
        print('DRY RUN! No, paths will be created.')
    if not os.path.exists(template):
        template = os.path.join(template_path, template)

    template = open(template).read()
    kwargs = {v[0]: v[1] if len(v) == 2 else v[1:] for v in mapping}
    tree = make_tree(template, **kwargs)

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
    parser.add_argument('-m', '--mapping', nargs='+', action='append',
                        help='key, value mapping pairs to fill in template')
    parser.add_argument('-d', '--dry-run', dest='dry_run', help=('Print directories that will be created, but'
                                                                 "don't create them"),
                        action='store_true')
    parser.set_defaults(dry_run=False)

    main(**vars(parser.parse_args()))
