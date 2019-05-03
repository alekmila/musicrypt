from django.urls import path

from base import views


two = lambda x: (x, x)


urlpatterns = [
    # Views
    path('', views.EncryptedFileListView.as_view(), name='encryptedfile_list'),
    path('detail/<int:pk>/', views.EncryptedFileDetailView.as_view(), name='encryptedfile_detail'),
    path('download/', views.download, name='encryptedfile_download'),

    path('upload/', views.EncryptedFileCreateView.as_view(), name='encryptedfile_create'),
] + [
    # Template files
    path(x, views.render(x)) for x in [
        '404.html',
    ]
] + [
    # Static files
    path(x, views.redirect(x)) for x in [
        'browserconfig.xml',
        'favicon.ico',
        'humans.txt',
        'icon.png',
        'robots.txt',
        'site.webmanifest',
    ]
]
