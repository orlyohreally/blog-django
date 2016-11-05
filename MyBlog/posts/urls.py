from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    about_page,
    search_tag,
    comment_create,
    comment_update,
    comment_delete,
	signin_user,
	login_user,
	logout_user
)

urlpatterns = [
    url(r'^$', post_list, name = 'list'),
    url(r'^comment/(?P<slug>[-\w]+)/(?P<id>[0-9]+)/edit$', comment_update, name = 'comment_update'),
    url(r'^comment/(?P<slug>[-\w]+)/(?P<id>[0-9]+)/delete$', comment_delete, name = 'comment_delete'),
    url(r'^about-MyBlog', about_page, name = 'about_page'),
    url(r'^create$', post_create),
    url(r'^search/(?P<tag>[-\w]+)', search_tag),
    url(r'^signin', signin_user),
    url(r'^login', login_user),
    url(r'^logout', logout_user),
	url(r'^(?P<slug>[-\w]+)$', post_detail, name = 'detail'),
    url(r'^(?P<slug>[-\w]+)/comment$', comment_create, name = 'comment_create'),
    url(r'^(?P<slug>[-\w]+)/edit/$', post_update, name = 'update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', post_delete),
    
	
    
]
