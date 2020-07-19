from  django.urls import path
from django.contrib.auth import views as auth_views
from  .import views
urlpatterns = [

    path('register/',views.registerPage,name="register"),
    path('user/',views.UserPage,name="user"),
    path('accountSetting',views.accountSetting,name='accountSetting'),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path("home/",views.home,name='home'),
    path("products/",views.products,name='products'),
    path("customer/<str:pk_test>/",views.customer,name='customer'),
    path('main/',views.main),
    path('status/',views.status),
    path('create/<str:pk>/',views.createOrder,name='create'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete/<str:pk>/',views.deleteOrder,name='delete'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_done.html'),name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done'), name="password_reset_complete"),



]