from django.core.exceptions import ValidationError



def validate_video_file_size(value):
    filesize = value.size
    
    # 2.5MB - 2621440
    # 5MB - 5242880
    # 10MB - 10485760
    # 20MB - 20971520
    # 50MB - 5242880
    # 100MB - 104857600
    # 250MB - 214958080
    # 500MB - 429916160
    
    if filesize > 104857600:
        raise ValidationError("You cannot upload file more than 100Mb")
    
def validate_file_size(value):
    filesize = value.size
    
    # 2.5MB - 2621440
    # 5MB - 5242880
    # 10MB - 10485760
    # 20MB - 20971520
    # 50MB - 5242880
    # 100MB - 104857600
    # 250MB - 214958080
    # 500MB - 429916160
    
    if filesize > 2621440:
        raise ValidationError("You cannot upload file more than 2.5Mb")