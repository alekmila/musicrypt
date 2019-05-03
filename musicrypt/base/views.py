import io
import os
import tempfile

from django import forms
from django import http
from django import shortcuts
from django.conf import settings
from django.core.files import uploadedfile
from django.views import generic
from django.views import static

from base import crypto
from base import models


def render(s):
    def f(request):
        return shortcuts.render(request, 'base/{}'.format(s), {})
    return f


def redirect(s):
    def f(request, *args, **kwargs):
        url = '{}{}'.format(settings.STATIC_URL, s)
        return shortcuts.redirect(url)
    return f


class EncryptedFileListView(generic.ListView):
    model = models.EncryptedFile
    ordering = '-pk'


# index = render('index.html')
# index = EncryptedFileListView.as_view()


class EncryptedFileDetailView(generic.DetailView):
    model = models.EncryptedFile


def download(req):
    pk = req.POST['pk']
    pwd = req.POST['password']
    obj = models.EncryptedFile.objects.get(pk=pk)  # Fetches id and filename from the database

    if not pwd:
        resp = static.serve(req, obj.encrypted.path, '/')
    else:
        # First decrypt the stored file using the password provided.  This
        # is done by creating a temporary file (which is not deleted later
        # -- TODO!) and then serving it.
        with open(obj.encrypted.path, 'rb') as inp:
            raw = inp.read()
        try:
            # DECRYPTING!!!
            dec = crypto.decrypt(raw, pwd)
        except:
            raise http.Http404('Error while decrypting.  Check password!')
        fn = tempfile.mkstemp()[1]
        with open(fn, 'wb') as out:
            out.write(dec)
        resp = static.serve(req, fn, '/')
    resp['Content-Disposition'] = 'attachment; filename={}'.format(
        obj.encrypted.name
    )
    return resp


# https://stackoverflow.com/questions/13550515/django-add-extra-field-to-a-modelform-generated-from-a-model
class CustomForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = models.EncryptedFile
        fields = ('encrypted',)

    def save(self, commit=True):
        # # Do something with self.cleaned_data['password']w
        # password = self.cleaned_data['password']
        # if not password:
        #     return super().save(commit)
        return super().save(commit)


class EncryptedFileCreateView(generic.CreateView):
    model = models.EncryptedFile
    form_class = CustomForm
    # fields = ('encrypted',)
    success_url = '/'

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            plain = kw['files']['encrypted']
            raw = plain.read()

            password = 'hello'
            # ENCRYPTING!!!
            encrypted = crypto.encrypt(raw, password)
            stream = io.BytesIO(encrypted)

            up = uploadedfile.InMemoryUploadedFile(
                stream,
                'encrypted',
                plain.name,
                plain.content_type,
                len(encrypted),
                plain.charset
            )
            kw['files']['encrypted'] = up
        return kw
