import os
from pypinyin import pinyin, Style

def chinese_to_pinyin_camelcase(text):
    """
    将中文字符转换为无空格camelCase格式的拼音
    """
    pinyin_list = pinyin(text, style=Style.NORMAL)
    camelcase = ''
    for i, word in enumerate(pinyin_list):
        if i == 0:
            camelcase += word[0]
        else:
            camelcase += word[0].capitalize()
    return camelcase

def rename_files_and_dirs(root_path):
    """
    递归遍历目录，重命名所有包含中文的文件和目录
    """
    for root, dirs, files in os.walk(root_path, topdown=False):
        # 先处理文件
        for name in files:
            if any('\u4e00' <= c <= '\u9fff' for c in name):
                old_path = os.path.join(root, name)
                basename, ext = os.path.splitext(name)
                new_basename = chinese_to_pinyin_camelcase(basename)
                new_name = new_basename + ext
                new_path = os.path.join(root, new_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed file: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming file {old_path}: {e}")

        # 然后处理目录
        for name in dirs:
            if any('\u4e00' <= c <= '\u9fff' for c in name):
                old_path = os.path.join(root, name)
                new_name = chinese_to_pinyin_camelcase(name)
                new_path = os.path.join(root, new_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed directory: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming directory {old_path}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)
    
    print(f"Starting to rename files and directories in: {directory}")
    rename_files_and_dirs(directory)
    print("Process completed.")
