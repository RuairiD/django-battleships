from django.conf.urls import url
from base.views import HomeView
from base.views import LoginView
from base.views import LogoutView
from base.views import SignupView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^signup$', SignupView.as_view(), name='signup'),
]