from django.urls import path
from . import views
app_name = "CAadmin"

urlpatterns = [
    path("login", views.login, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("contact-us", views.contact_us, name="contact_us"),
    path("client-edit", views.client_edit, name="client_edit"),
    path("CAsignup", views.ca_signup, name="ca_signup"),
]
