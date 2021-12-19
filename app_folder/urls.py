from django.urls import path
from . import views

urlpatterns = [
    path('',views.mainpage),
    path('success',views.success),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('add_favorite_quote',views.add_favorite_quote),
    path('all_quotes_by_user/<int:quote_added_by_id>',views.all_quotes_by_user),
    path('like_quote/<int:quote_id>/<int:page_number>',views.like_quote),
    path('delete_quote/<int:quote_id>/<int:page_number>',views.delete_quote),
    path('display_user_information',views.display_user_information), 
    path('edit_user_information',views.edit_user_information),
    path('update_user_information',views.update_user_information),
]