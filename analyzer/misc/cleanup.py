import os
import shutil

from analyzer.config.config import Config


def cleanup_cache_files(config: Config):
    """
    To be used at bot exit, if enabled
    """
    file_extensions = config.CLEANUP_extensionS
    directories = config.CLEANUP_DIRS

    root = config.ROOT_DIR

    dir_count = 0
    file_count = 0

    if os.path.exists(root) and config.CLEANUP_ENABLED:
        if os.path.isdir(root):
            for root_folder, folders, files in os.walk(root):
                for folder in folders:
                    folder_path = os.path.join(root_folder, folder)
                    if folder in directories:
                        try:  # empty directories
                            os.rmdir(folder_path)
                            dir_count += 1
                        except Exception:
                            try:  # non-empty directories
                                shutil.rmtree(folder_path)
                                dir_count += 1
                            except Exception:
                                print(f"Unable to purge directory: {folder_path}")
                for file in files:
                    file_path = os.path.join(root_folder, file)
                    extension = os.path.splitext(file_path)[1]
                    if extension in file_extensions and os.path.isfile(file):
                        try:
                            os.remove(file_path)
                            file_count += 1
                        except Exception:
                            print(f"Unable to purge file: {file_path}")
        else:
            print(f"{root} is not a directory")
    else:
        print(f"{root} doesn't exist")
    print(f"Purged {dir_count} directories, and {file_count} files")
