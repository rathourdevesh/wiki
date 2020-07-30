from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/",views.wikipage,name="wikipage"),
    path("search",views.search,name="searchpage"),
    path("newentry",views.new_entry,name="newentry"),
    path("random",views.Random_page,name="randompage"),
    path("editEntry/<str:title>/",views.edit_entry,name="editEntry")
]
