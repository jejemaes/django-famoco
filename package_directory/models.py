import os
import time
import uuid

from django.contrib import admin
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import FileExtensionValidator


def app_directory_path(instance, filename):
    unique_name = '%s%s' % (filename, time.time())
    return str(uuid.uuid3(uuid.NAMESPACE_URL, unique_name)) + '.apk'


class Application(models.Model):

    apk_file = models.FileField(upload_to=app_directory_path, validators=[FileExtensionValidator(['apk'])])
    package_name = models.CharField(max_length=42)
    package_version_code = models.CharField(max_length=10)
    create_date = models.DateTimeField(default=timezone.now, verbose_name="Date de creation")
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Application Android"
        ordering = ['package_name']
    
    def __str__(self):
        return self.package_name



@receiver(models.signals.post_delete, sender=Application)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.apk_file:
        if os.path.isfile(instance.apk_file.path):
            os.remove(instance.apk_file.path)

@receiver(models.signals.pre_save, sender=Application)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).apk_file
    except sender.DoesNotExist:
        return False

    new_file = instance.apk_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

# ------------------------------------------------------------
# Admin Model
# ------------------------------------------------------------

class ApplicationAdmin(admin.ModelAdmin):
    list_display   = ('apk_file', 'package_name', 'package_version_code', 'description')
    list_filter    = ('package_name','package_version_code',)
    date_hierarchy = 'create_date'
    ordering       = ('package_name', )
    search_fields  = ('package_name', 'package_version_code')

    readonly_fields = ('create_date',)
