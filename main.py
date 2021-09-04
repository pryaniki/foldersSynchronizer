import os
import sys
import time
import json
import inotify.adapters
import shutil
import processing_changes as proc_change
# from inotify_simple import INotify, flags

from shutil import copyfile

from completedFunctions import checkingProgPerformance, checkOS, readConfig, \
    isOnList, removeDuplicatesFromList, deletingFilesAndFolders

### добавить случай с сылкой
def sync(root, paths, folder_to_syn):
    import processing_changes as pc
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
                # print('create file ', current_path)
                if os.path.islink(folder_to_syn + os.sep + path):
                    pc.creat_link(folder_to_syn + os.sep + path, current_path)
                else:
                    copyfile(folder_to_syn + os.sep + path, current_path)
        elif rec[0] == 'd':
            if not os.path.isdir(current_path):
                if os.path.islink(folder_to_syn + os.sep + path):
                    pc.creat_link(folder_to_syn + os.sep + path, current_path)
                else:
                    os.mkdir(current_path)
                    # print("create dir  ", current_path)



def traverse(root, pref, dir_ignore_syn, depth=0):
    result = dict()
    try:
        names = os.listdir(root)
    except FileNotFoundError:
        return
    for name in names:
        current_path = root + os.sep + name
        # if not dir_ignore_syn is None:
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
    return p.startswith('.')  # linux-osx


def сhecking_folder_changes(inotif, changes, pref):
    """
    Функция отслеживает изменения в директории pref и
    возвращает словарь формата [флаг, путь к измененному файлу без префикса pref] [фдаг изменения, время изменения файла ]

    Флаг изменения может принимать 3 состоянияж
    - "mod" - объект изменяется
    - "cha" - объект создан
    - "del" - объект удален
    """
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
    events = inotif.event_gen(yield_nones=False, timeout_s=3)
    events = list(events)
    print_it = False
    for elem in events:
        for command in elem[1]:
            if isOnList(interest_flags, command):
                if print_it:
                    print('----------------------')
                    print_it = False
                current_path = str(elem[2]) + os.sep + str(elem[3])


                if not folder_is_hidden(current_path[:]) and current_path[-5:] != ".part" and current_path[
                                                                                           -9:] != ".kate-swp":
                    modification = [elem[1][0], current_path[len(pref) + 1:]]
                    if isOnList(delete_flag, command):  # файл удален
                        changes[str(modification)] = ['del', 0]
                    elif isOnList(create_flag, command):  # файл создан
                        changes[str(modification)] = ['cre', int(os.path.getmtime(current_path))]
                    elif isOnList(modific_flag, command):  # файл изменен
                        changes[str(modification)] = ['mod', int(os.path.getmtime(current_path))]
                    # modification.append(int(os.path.getmtime(current_path)))
    return changes


def emptydir(top):
    if top == os.sep:
        return
    else:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                if os.path.islink(path):
                    os.unlink(path)
                else:
                    os.remove(path)
            for name in dirs:
                path = os.path.join(root, name)
                if os.path.islink(path):
                    os.unlink(path)
                else:
                    os.rmdir(path)

def copy_folder(f_from, f_to):
    from completedFunctions import getListDirAndFiles
    import processing_changes as pc

    if not os.path.exists(f_to):
        pc.creat_folder(f_to)

    folderPaths, filePaths = getListDirAndFiles(f_from)
    pref = os.path.commonprefix(folderPaths)

    for folder in folderPaths:
        current_path = f_to + folder[len(pref)-1:]
        if os.path.islink(folder):
            pc.creat_link(folder, current_path)
        else:
            pc.creat_folder(current_path)


    for file in filePaths:
        current_path = f_to + file[len(pref)-1:]
        if os.path.islink(file):
            pc.creat_link(file, current_path)
        else:
            pc.copy_file(file, current_path)


def restore_folders_to_original_state(backup, folder_to_change):
    """
    Функция полностью очищает папку folder_to_change и переносит в нее файлы из backup
    """
    if not os.path.exists(folder_to_change):
        copy_folder(backup, folder_to_change)
    else:
        if os.path.isdir(backup) and os.path.isdir(folder_to_change):
            emptydir(folder_to_change)
            os.rmdir(folder_to_change)
            copy_folder(backup, folder_to_change)
            #shutil.copytree(backup, folder_to_change)
        else:
             print(f"{backup}\n или {folder_to_change}\n не являются директорией")


def primary_syn(names):
    """
    Функция проводит первичную синхронизацию папок.
    Содержимое из 1-ой папки Config дублируется в остальные
    """
    deletingFilesAndFolders(names)
    dir_ignore_syn = get_dir_ignore_syn(names[0], names[1:])

    paths = traverse(names[0], names[0], dir_ignore_syn)
    folder_to_syn = names[0]
    for name in names[1:]:
        # if not name.startswith(names[0]):
        sync(name, paths, folder_to_syn)


def test():
    pass


def main():

    backup = "/run/media/maks/Soft/Programs/My_programs/foldersSynchronizer/backup/"
    folder_to_change = "/run/media/maks/Soft/Programs/My_programs/foldersSynchronizer/Tests"
    restore_folders_to_original_state(backup, folder_to_change)

    with open(sys.argv[1], 'r') as file:
        names = json.loads(file.read())

    primary_syn(names)

    pref = os.path.commonpath(names)  # общий префикс всех путей из списка
    changes = {}

    folder_content = {}  # Содержимое папок из конфига

    folders_in_config = []  # Список папок из конфига без префикса
    for folder in names:
        folder_content[folder[len(pref) + 1:]] = traverse(folder, folder, [])

        folders_in_config.append(folder[len(pref) + 1:])

    print(f"отслеживаю изменения в {pref}\n")
    while True:
        inotif = inotify.adapters.InotifyTree(pref)

        time.sleep(1)  # задержка проверки на изменеия в папках
        changes.update(
            сhecking_folder_changes(inotif, changes, pref))  # если синхронизация прошла успешно, то очистить словарь

        #  Снавнить время изменения файла во всех папках конфига
        #  если он свежее в верхней папке, то оставляем его, есле же он удален в верхней папке, то удоляем отовсюду
        if changes:
            proc_change.clearing(changes, folders_in_config)
            start_syn(changes, folders_in_config, folder_content, pref)
        print_it = False
        if print_it:
            print(f'list_changes:\n')
            for elem in changes:
                print(f'{elem} {changes[elem]}')
            print("-----")


def start_syn(changes: dict, folders_in_config: list, folder_content: dict, pref: str):
    """
    Функция обрабатывает все изменения из changes
    """

    for id, value in list(changes.items()):

        print(f"\nобработка изменения {id}, {value}")
        path = id.split(',')[1][2:-2]
        changed_folder = max(list(
            map(lambda path_config: os.path.commonpath([path, path_config]),
                folders_in_config)))  # Папка, в которой произошли изменения

        path_to_modified_object = path[len(changed_folder):]  # путь к изменненому файлу \ папке

        flag = value[0]  # "del"\"cre"\"mod"

        if flag == "del":

            for folder in folders_in_config:
                path_need_to_delete = pref + os.sep + folder + path_to_modified_object
                #print(f" path_need_to_delete { path_need_to_delete}")
                #print(f"{folder + path_to_modified_object}")
                if os.path.isdir(path_need_to_delete) and \
                        isOnList(folders_in_config, folder + path_to_modified_object):  # Если удалена папка из print(f"Надо удалить {path_need_to_delete}")
                    sys.exit(f"Папка {pref + os.sep + path} \nиз списка {sys.argv[1]}"
                             f" была удалена, программа не может работать дальше")
                else:  # удоляем
                    if folder != changed_folder:  # не учитываю папку, в которой произошли изменения
                        if os.path.islink(path_need_to_delete):
                            proc_change.deleting_link(path_need_to_delete)
                        elif os.path.isfile(path_need_to_delete):
                            proc_change.deleting_file(path_need_to_delete)
                        elif os.path.isdir(path_need_to_delete):
                            proc_change.deleting_directory(path_need_to_delete)

        elif flag == "cre":
            for folder in folders_in_config:
                path_need_for_copy = pref + os.sep + path  # копируем файл\папку во все папки

                if folder != changed_folder:  # не учитываю папку, в которой произошли изменения
                    path_to_copy = pref + os.sep + folder + path_to_modified_object
                    print(f"копировать \n{path_need_for_copy} \nв папку \n{path_to_copy}")
                    if os.path.islink(path_need_for_copy):
                        proc_change.creat_link(path_need_for_copy, path_to_copy)
                    elif os.path.isfile(path_need_for_copy):
                        proc_change.copy_file(path_need_for_copy, path_to_copy)
                    elif os.path.isdir(path_need_for_copy):
                        proc_change.creat_folder(path_to_copy)

        elif flag == "mod":
            for folder in folders_in_config:
                path_need_for_replacement = pref + os.sep + path  # Произошли изменения
                print(f"копировать {path_need_for_replacement}")
                if folder != changed_folder:  # не учитываю папку, в которой произошли изменения
                    path_to_change = pref + os.sep + folder + path_to_modified_object
                    if os.path.islink(path_need_for_replacement):
                        print(f"модифицированна ссылка {path_need_for_replacement}")
                    elif os.path.isfile(path_need_for_replacement):
                        proc_change.change_file(path_need_for_replacement, path_to_change)
                    elif os.path.isdir(path_need_for_replacement):
                        print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/ {path_need_for_replacement} c флогом mod")

        # если все прошло без ошибок
        if True:
            del changes[id]


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
