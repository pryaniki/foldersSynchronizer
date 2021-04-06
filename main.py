import os
import sys
import time
import json
import inotify.adapters
import shutil
#from inotify_simple import INotify, flags

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
                    pass
                    # print('update file', current_path)
            elif os.path.isdir(current_path):
                pass  # имя занято директорией - надо удалить папку или пропустить
            else:
                pass
                # print('create file ', current_path)
                # copyfile(folder_to_syn+os.sep+path, current_path)

        elif rec[0] == 'd':
            if not os.path.isdir(current_path):
                # os.mkdir(current_path)
                pass
                # print("create dir  ", current_path)


def traverse(root, pref, dir_ignore_syn, depth=0):
    result = dict()
    try:
        names = os.listdir(root)
    except FileNotFoundError:
        return
    for name in names:
        current_path = root + os.sep + name
        if not isOnList(dir_ignore_syn, current_path):
            # print(current_path)
            sync_path = name
            if depth > 0:
                sync_path = root + os.sep + name
                if not sync_path.find(pref):
                    sync_path = sync_path[len(pref) + 1:]
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
            if i + 1 == j:
                continue
            elif os.path.commonpath([path, paths[j]]) == path:
                result.append(paths[j])

    return removeDuplicatesFromList(result)

def folder_is_hidden(p):
     return p.startswith('.') #linux-osx

def сhecking_folder_changes(inotif, changes, pref):
    # IN_ATTRIB — Изменены метаданные (права, дата оздания/редактирования, расширенные атрибуты, и т.д.)
    # IN_CREATE — Файл/директория создан(а) в отслеживаемой директории
    # IN_DELETE — Файл/директория удален(а) в отслеживаемой директории
    # IN_DELETE_SELF — Отслеживаемый(ая) файл/директория был(а) удален(а)
    # IN_MODIFY — Файл был изменен
    # IN_MOVE_SELF — Отслеживаемый(ая) файл/директория был(а) перемещен(а)
    # IN_MOVED_FROM — Файл был перемещен из отслеживаемой директории
    # IN_MOVED_TO — Файл перемещен в отслеживаемую директорию
    interest_flags = ['IN_ATTRIB', 'IN_MODIFY',
                      'IN_DELETE_SELF', 'IN_DELETE', 'iN_MOVE_SELF', 'IN_MOVED_FROM',
                      'IN_MOVED_TO', 'IN_CREATE']  # Подходящие флаги
    modific_flag, delete_flag, create_flag = interest_flags[:2], interest_flags[2:6], interest_flags[-2:]
    events = inotif.event_gen(yield_nones=False, timeout_s=1)
    events = list(events)
    print_it = True
    for elem in events:
        for command in elem[1]:
            if isOnList(interest_flags, command):
                if print_it:
                    print('----------------------')
                    print_it = False
                current_path = str(elem[2])+os.sep+str(elem[3])

                if not folder_is_hidden(current_path) and current_path[-5:]!=".part" and current_path[-9:] != ".kate-swp":
                    modification = [elem[1][0], current_path[len(pref)+1:]]
                    print(f'command {command}')
                    print(f'modif {modification}')
                    if isOnList(delete_flag, command):  # файл удален
                        changes[str(modification)] = ['d', 0]
                    elif isOnList(create_flag, command):  # файл создан
                        changes[str(modification)] = ['c', int(os.path.getmtime(current_path))]
                    elif isOnList(modific_flag, command):  # файл изменен
                        changes[str(modification)] = ['m', int(os.path.getmtime(current_path))]
                    #modification.append(int(os.path.getmtime(current_path)))
    return changes

def emptydir(top):
    if(top == '/' or top == "\\"): return
    else:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def restore_folders_to_original_state():
    from completedFunctions import getListDirAndFiles
    names = os.listdir("/run/media/maks/Soft/Programs/My_programs/foldersSynchronizer/Tests/")

    import sh
    emptydir('/run/media/maks/Soft/Programs/My_programs/foldersSynchronizer/Tests/')
    os.rmdir('/run/media/maks/Soft/Programs/My_programs/foldersSynchronizer/Tests/')

    folder_from = "/run/media/maks/Soft/Programs/My_programs/foldersSynchronizer/backup/"
    folder_to = "/run/media/maks/Soft/Programs/My_programs/foldersSynchronizer/Tests/"
    shutil.copytree(folder_from, folder_to)


def main():
    restore_folders_to_original_state()
    with open(sys.argv[1], 'r') as file:
        names = json.loads(file.read())
        deletingFilesAndFolders(names)
        dir_ignore_syn = get_dir_ignore_syn(names[0], names[1:])
        pref = os.path.commonpath(names)
        changes = dict()
        #changes = []
        print_it = True


        paths = traverse(names[0], names[0], dir_ignore_syn)
        folder_to_syn = names[0]
        for name in names[1:]:
            # if not name.startswith(names[0]):
            sync(name, paths, folder_to_syn)


        folder_content_properties = {} #  свойства содержимого папок
        for folder in names:
            folder_content_properties[folder[len(pref)+1:]] = traverse(folder, folder, [])
        for i in folder_content_properties:
            print(f'{i} *** {folder_content_properties[i]}')


    pref ='/run/media/maks/Soft/Programs/My_programs/FS/tmp' # УДАЛИТЬ

    while True:
        inotif = inotify.adapters.InotifyTree(pref)

        #changes = сhecking_folder_changes(inotif, changes, pref).copy()
        time.sleep(2)
        changes.update(сhecking_folder_changes(inotif, changes, pref)) # если синхронизация прошла успешно, то очистить словарь
        if print_it:
            print(f'list_changes:\n')
            for elem in changes:
                print(f'{elem} {changes[elem]}')
            print("-----")
            #print_it = False
        #break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
