from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.search, name='homepage'),
    url(r'^search/$', views.search, name='search'),
    url(r'^results/$', views.results, name='results'),
    url(r'^tool/(?P<tool_id>[0-9]+)/$', views.tool, name='tool'),
    url(r'^my-tools/$', views.my_tools, name='my_tools'),
    url(r'^add-tool/$', views.add_tool, name='add_tool'),
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^add-dependencytag/$', views.add_dependencytag, name='add_dependencytag'),
    url(r'^add-businesstag/$', views.add_businesstag, name='add_businesstag'),
    url(r'^edit-tool/(?P<tool_id>[0-9]+)/$', views.edit_tool, name='edit_tool'),
    url(r'^delete-tool/(?P<tool_id>[0-9]+)/$', views.delete_tool, name='delete_tool'),
    url(r'^transfer-tool/(?P<tool_id>[0-9]+)/$', views.transfer_tool, name='transfer_tool'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact-devs/$', views.contact_devs, name='contact_devs'),
    url(r'^users/$', views.find_users, name='find_users'),
]
