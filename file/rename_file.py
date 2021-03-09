from pathlib import Path


def rename(root: str, base_name: str, skip_dir: bool = True):
    """重命名目录下的所有文件

    根据base_name重命名文件，按照次序修改名字，保留文件后缀，所有文件均放置在同一级目录下
    :param skip_dir: 重命名是否跳过目录
    :param root: 根目录
    :param base_name: 基础名称
    """
    root_file = Path(root)
    for i, file in enumerate(root_file.rglob('*'), 0):
        if skip_dir and file.is_dir():
            continue

        parent = file.parent

        if '.' in str(file.name):
            suffix = str(file.name).split('.')[-1]
            file.rename(str(parent.absolute()) + '/' + base_name + str(i) + '.' + suffix)
            print('rename % successfully' % str(file.name))
        else:
            file.rename(str(parent.absolute()) + '/' + base_name + str(i))
            print('rename % successfully' % str(file.name))


if __name__ == '__main__':
    rename('/Users/apple/Downloads/图片/锈蚀', '锈蚀')
