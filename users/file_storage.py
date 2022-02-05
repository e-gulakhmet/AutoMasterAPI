import os


def get_storage_path_static(key, filename, directory):
    return f"{directory}/{key}/{filename}"


def avatar_property_avatar_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return get_storage_path_static(instance.pk, f"avatar{file_extension}", 'avatars')