"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from libraryapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', views.welcome, name = "home_page"),
    path('books/',views.show_books, name = "active_books" ),
    path('update/<int:id>/', views.update_book, name= "update_book"),        # parameter passing for update_book view is id
    path('harddelete/<int:id>/', views.harddelete_book, name="harddelete_book"),
    path('softdelete/<int:id>/', views.softdelete_book, name="softdelete_book"),
    path('inactive-books/',views.show_inactive_books, name = "inactive_books" ),
    path('restore-book/<int:id>/',views.restore_book, name = "restore_book" ),
    path('index/', views.index, name = "index"),
    path('cbv-book-create',views.BookCreate.as_view(), name = 'BookCreate'),
    path('retrieve/', views.BookRetrieve.as_view(), name = 'BookRetrieve'),
    path('retrieve/<int:pk>/', views.BookDetail.as_view(), name="BookDetail"),
    path('update/<int:pk>/', views.UpdateView.as_view(), name="UpdateView"),
    path('delete/<int:pk>/', views.BookDelete.as_view(), name="BookDelete"),
    path('template', views.BookTemplate.as_view(), name="BookTemplate"),
    path('book_form/', views.book_form, name="book_form"),
    
]  
   
   

