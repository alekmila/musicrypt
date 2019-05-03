import os

from django.db import models


class EncryptedFile(models.Model):
    encrypted = models.FileField(upload_to='base/encrypted/%Y/%m/%d/')

    def __str__(self):
        return os.path.split(self.encrypted.name)[1]

    '''
    def get_absolute_url(self):
        from django import urls
        return urls.reverse('encryptedfile_detail', args=(str(self.pk),))
    '''
