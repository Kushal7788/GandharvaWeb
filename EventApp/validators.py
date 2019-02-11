from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 25165824:
        raise ValidationError("The maximum file size that can be uploaded is 25kB")
    else:
        return value
