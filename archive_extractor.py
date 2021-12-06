#!/usr/bin/python3

import os, zipfile, tarfile, gzip, shutil, lzma


class colors:
    FAIL = '\033[91m'
    END = '\033[0m'


failed_items = []


def extract_arch(full_arch_name, extractor):
    print("Extracting archive: ", full_arch_name)
    subdir = os.path.splitext(full_arch_name)[0]
    failed = False
    try:
        with extractor(full_arch_name) as ex:
            try:
                ex.extractall(subdir)
            except:
                print(colors.FAIL, "FAIL", colors.END)
                failed_items.append(full_arch_name)
                failed = True
    except:
        print(colors.FAIL, "FAIL", colors.END)
        failed_items.append(full_arch_name)
        failed = True
    if not failed:
        os.remove(full_arch_name)
    extract_all(subdir)


def extract_file(full_filename, file_opener):
    print("Extracting file: ", full_filename)
    failed = False
    try:
        with file_opener.open(full_filename, 'rb') as arch_file:
            with open(os.path.splitext(full_filename)[0], 'wb') as file:
                shutil.copyfileobj(arch_file, file)
    except:
        print(colors.FAIL, "FAIL", colors.END)
        failed_items.append(full_filename)
        failed = True
    if not failed:
        os.remove(full_filename)


def extract_all(dirname):
    for root, _, files in os.walk(dirname):
        for file in files:
            if file.endswith(".zip"):
                extract_arch(os.path.join(root, file), zipfile.ZipFile)
            elif file.endswith(".tar"):
                extract_arch(os.path.join(root, file), tarfile.TarFile)
            elif file.endswith(".gz"):
                extract_file(os.path.join(root, file), gzip)
            elif file.endswith(".xz"):
                extract_file(os.path.join(root, file), lzma)


extract_all(".")

if len(failed_items) > 0:
    print(colors.FAIL, "Failed items:", colors.END)
    for item in failed_items:
        print(colors.FAIL, "\t", item, colors.END)

