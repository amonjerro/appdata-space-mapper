from operator import indexOf
import os

APP_DATA_PATH = os.getenv('APPDATA')
ROOT_APP_DATA_PATH = APP_DATA_PATH[:APP_DATA_PATH.index('Roaming')]

CONVERSIONS = {
    'K':1024,
    'M':1024**2,
    'G':1024**3
}

def get_file_size(filename, conversion):
    return os.stat(filename).st_size / CONVERSIONS[conversion]

def scan(in_path):
    size = 0
    if '.' in in_path:
        return get_file_size(in_path,'M')
    try:
        files = os.scandir(in_path)
        for file in files:
            if file.is_file() or file.name[-2:] == 'db':
                size += get_file_size(f'{in_path}\{file.name}','M')
            else:
                size += scan(f'{in_path}\{file.name}')
        return size
    except PermissionError:
        print(in_path)
        return 0

def make_groups():
    horizon = os.listdir(ROOT_APP_DATA_PATH)
    root_groups = { k:{} for k in horizon }
    for k in horizon:
        root_groups[k] = {f:0 for f in os.listdir(f'{ROOT_APP_DATA_PATH}\{k}')}

    return root_groups

total_memory = 0
groups = make_groups()
for g in groups.keys():
    for i in groups[g].keys():
        scan_result = scan(f'{ROOT_APP_DATA_PATH}\{g}\{i}')
        groups[g][i] = scan_result
        total_memory += scan_result

print('Total Memory:', total_memory)

# Remove useless keys
keys_to_remove = []
for g in groups.keys():
    for i in groups[g].keys():
        if groups[g][i] < 100:
            keys_to_remove.append((g,i))

for g, i in keys_to_remove:
    del groups[g][i]

for g in groups.keys():
    print(groups[g])