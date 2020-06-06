from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms.widgets import FileInput


class ImageInput(FileInput):
    """
    Widget providing a input element for file uploads based on the
    Django ``FileInput`` element. It hides the actual browser-specific
    input element and shows the available image for images that have
    been previously uploaded. Selecting the image will open the file
    dialog and allow for selecting a new or replacing image file.
    """
    template_name = 'forms/widgets/image_input_widget.html'

    def __init__(self, attrs=None):
        if not attrs:
            attrs = {}
        attrs['accept'] = 'image/*'
        super(ImageInput, self).__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        ctx = super(ImageInput, self).get_context(name, value, attrs)

        ctx['image_url'] = ''
        if value and not isinstance(value, InMemoryUploadedFile):
            # can't display images that aren't stored - pass empty string to context
            ctx['image_url'] = value

        ctx['image_id'] = "%s-image" % ctx['widget']['attrs']['id']
        return ctx
