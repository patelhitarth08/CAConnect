from django.urls import path
from . import views
app_name = "CAadmin"

urlpatterns = [
    path("login", views.login, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("contact-us", views.contact_us, name="contact_us"),
    path("client-add", views.client_add, name="client_add"),
    path("client-list", views.client_list, name="client_list"),
    path("client-detail/<int:client_id>",
         views.client_detail, name="client_detail"),
    path("client-edit/<int:client_id>",
         views.client_edit, name="client_edit"),
    path("delete_client/<int:client_id>",
         views.delete_client, name="delete_client"),
    path("toggle_status", views.toggle_status, name="toggle_status"),
    path("CAsignup", views.ca_signup, name="ca_signup"),
]
