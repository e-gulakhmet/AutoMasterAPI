from rest_framework.exceptions import ValidationError


def check_if_file_size_is_out_of_limit(file_size: int, file_size_limit_mb: int) -> bool:
    """ Return True if file size is out if limit """
    limit_kb = file_size_limit_mb * 1024 * 1024
    if file_size > limit_kb:
        return True
    return False


def validate_avatar_max_size(value):
    file_size_limit_mb = 10
    if check_if_file_size_is_out_of_limit(file_size=value.size, file_size_limit_mb=file_size_limit_mb):
        raise ValidationError("Maximum file size %s MB" % file_size_limit_mb)
