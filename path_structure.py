import os


def get_tree(folder, prefix=''):
    tree_str = ''
    files = sorted(os.listdir(folder))
    for index, file in enumerate(files):
        path = os.path.join(folder, file)
        is_last = index == len(files) - 1
        tree_str += prefix + ('└── ' if is_last else '├── ') + file + '\n'
        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            tree_str += get_tree(path, prefix=prefix+extension)
    return tree_str


if __name__ == '__main__':
    s = get_tree('.')
    print(s)