import os
import sys
import time
import json
from shutil import copyfile

from completedFunctions import checkingProgPerformance, checkOS, readConfig, \
    isOnList, removeDuplicatesFromList, deletingFilesAndFolders

def show_help():
    print('usage: python [CONFIG]')


def sync(root, paths, folder_to_syn):
    for path in paths:
        current_path = root + os.sep + path
        rec = paths[path]
        if rec[0] == 'f':
            if os.path.isfile(current_path):
                if rec[1] > int(os.path.getmtime(current_path)):
                    print('update file', current_path)
            elif os.path.isdir(current_path):
                pass  # имя занято директорией - надо удалить папку или пропустить
            else:
                #print('create file ', current_path)
                copyfile(folder_to_syn+os.sep+path, current_path)

        elif rec[0] == 'd':
            if not os.path.isdir(current_path):
                os.mkdir(current_path)
                #print("create dir  ", current_path)


def traverse(root, pref, dir_ignore_syn, depth=0):
    result = dict()
    try:
        names = os.listdir(root)
    except FileNotFoundError:
        return
    for name in names:
        current_path = root + os.sep + name
        if not isOnList(dir_ignore_syn, current_path):
            #print(current_path)
            sync_path = name
            if depth > 0:
                sync_path = root + os.sep + name
                if not sync_path.find(pref):
                    sync_path = sync_path[len(pref)+1:]
            if os.path.isfile(current_path):
                mtime = int(os.path.getmtime(current_path))
                result[sync_path] = ['f', mtime]
            elif os.path.isdir(current_path):
                mtime = int(os.path.getmtime(current_path))
                result[sync_path] = ['d', mtime]
                result.update(traverse(current_path, pref, dir_ignore_syn, depth + 1))
    return result


def get_dir_ignore_syn(pref, paths):
    result = []
    for path in paths[1:]:
        if os.path.commonpath([pref, path]) == pref:
            result.append(path)

    for i, path in enumerate(paths[1:]):
        for j in range(len(paths)):
            if i+1 == j:
                continue
            elif os.path.commonpath([path, paths[j]]) == path:
                result.append(paths[j])

    return removeDuplicatesFromList(result)


def test():
    for i in range(6):
        with open('Config'+str(i+1)+'.json', 'r') as file:
            names = json.loads(file.read())
            deletingFilesAndFolders(names)
            dir_ignore_syn = get_dir_ignore_syn(names[0], names)
            print('Config', i+1, dir_ignore_syn)

def main():
    #test()
    with open(sys.argv[1], 'r') as file:
        names = json.loads(file.read())
        deletingFilesAndFolders(names)
        dir_ignore_syn = get_dir_ignore_syn(names[0], names[1:])
        pref = os.path.commonpath((names))
    while True:
        paths = traverse(names[0], names[0], dir_ignore_syn )
        '''
        print("dict\n")
        for path in paths:
            print(path, paths[path])
        '''
        folder_to_syn = names[0]
        for name in names[1:]:
            #if not name.startswith(names[0]):
            sync(name, paths, folder_to_syn)
        #time.sleep(1)
        break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
