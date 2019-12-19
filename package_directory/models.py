import os
import re
import time
import uuid

from django.contrib import admin
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.files.uploadedfile import TemporaryUploadedFile


def app_directory_path(instance, filename):
    unique_name = '%s%s' % (filename, time.time())
    return str(uuid.uuid3(uuid.NAMESPACE_URL, unique_name)) + '.apk'

def extract_apk_package_data(path):
    cmd = """aapt dump badging %s | grep versionName""" % (path,)
    response_str = os.popen(cmd).read()

    match = re.compile("package: name='(\\S+)' versionCode='(\\d+)' versionName='([0-9\\.\\s]+)'").match(response_str)
    if not match:
        raise Exception("can't get packageinfo")
    package_name = match.group(1)
    version_code = match.group(2)
    version_name = match.group(3)

    return {
       'package_name': package_name, 
       'package_version_code': version_code,
    }


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
    # modifiy package fields according to the APK extracted fields
    if instance:
        if instance.apk_file and isinstance(instance.apk_file.file, TemporaryUploadedFile):  # heuristic to say "we change the apk file"
            pkg_data = extract_apk_package_data(instance.apk_file.file.temporary_file_path())

            for fname, value in pkg_data.items():
                if not instance.__dict__[fname]:
                    instance.__dict__[fname] = value  # instance[myfield] is not working, maybe we should use setattr 
    
    if not instance.pk:
        return False

    # remove the file that might not be linked to the db record
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
    fields   = ('apk_file', 'description')
    readonly_fields = ('package_version_code', 'package_name', 'create_date')

    list_display   = ('package_name', 'package_version_code', 'description')
    list_filter    = ('package_name','package_version_code',)
    date_hierarchy = 'create_date'
    ordering       = ('package_name', )
    search_fields  = ('package_name', 'package_version_code')

    def get_form(self, request, obj=None, **kwargs):
        """ When editing, the 2 packages fields should be visible """
        if obj:
            self.fields += ('package_name', 'package_version_code')
        form = super(ApplicationAdmin, self).get_form(request, obj, **kwargs)
        return form
