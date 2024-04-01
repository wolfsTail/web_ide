from django.urls import path

from editor import views


urlpatterns = [
    path('', views.get_editor, name="editor"),
    path('execute_code_partial/', views.execute_code_partial, name="execute_code"),
]