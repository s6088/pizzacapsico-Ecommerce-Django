from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size
    
    if filesize > 2400000:
        raise ValidationError("The maximum file size that can be uploaded is 300kb go https://compressjpeg.com/ to minify your image")
    else:
        return value
