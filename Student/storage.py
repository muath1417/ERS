import os

from django.core.files.storage import FileSystemStorage

from ERS import settings


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name,max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name