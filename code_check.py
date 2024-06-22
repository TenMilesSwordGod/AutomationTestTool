import os

from rich import print


def count_lines_in_folder(folder_path, extensions=('.py',)):
    total_lines = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1] in extensions:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if line.strip():
                            total_lines += 1
    return total_lines


cound_folder = ['att_fw', 'att_test_scripts', 'att_test_suites', 'att_testlib']
total_lines = 0

for folder in cound_folder:
    print(f"[purple bold]check folder: {folder}[/purple bold]")
    lines_count = count_lines_in_folder(folder)
    print("       [red bold]python total lines:{}[/red bold]".format(lines_count))
    total_lines += lines_count

print("[yellow bold][*] total lines: {}[/yellow bold]".format(total_lines))
