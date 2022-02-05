import os

from django.core.files import File


def get_file_name(file) -> str:
    file_name = file.name.split('\\')[-1]
    return file_name


def get_file_rb(filename, path) -> File:
    opened = open(os.path.join(path, filename), mode='rb')
    file = File(opened, get_file_name(opened))
    return file
