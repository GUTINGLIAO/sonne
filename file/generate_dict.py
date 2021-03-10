from pathlib import Path


def generate_labels(root: str, label: int):
    """为数据集生成标签

    写入文件形式为追加
    :param label: 目录下所有图片的标签
    :param root: 数据集所在目录
    """
    root_path = Path(root)
    labels_txt = Path('./labels.txt')

    with open(labels_txt, 'a') as f:
        for file in root_path.rglob('*'):
            if file.is_dir():
                continue

            f.writelines('%s %d\n' % (str(file.name), label))


if __name__ == '__main__':
    generate_labels('/Users/apple/Downloads/图片/train/龟裂', 3)
