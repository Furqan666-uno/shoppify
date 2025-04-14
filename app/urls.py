# this file was not pre-built
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm # this will help us create login page without passing it to views.py & creating class

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),

    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'), # here pk= primary key
    
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name="showcart"),

    path('pluscart/', views.plus_cart, name="pluscart"),
    path('minuscart/', views.minus_cart, name="minuscart"),
    path('removecart/', views.remove_cart, name="removecart"),
    
    path('buy/', views.buy_now, name='buy-now'),

    path('search/', views.search, name='search'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('mobile/', views.mobile, name='mobile'),
    path ('mobile/<slug:data>', views.mobile, name='mobiledata'),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name= 'app/login.html', authentication_form= LoginForm), name='login'), 
    # here we prefer to write path as 'accounts/login/
    # here authentication form is written as LoginForm from forms.py to link it to the path here, helps in html coding 
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # here next_page means the page will redirect to login page if we logout
    
    
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name= 'app/passwordchange.html', form_class= MyPasswordChangeForm, success_url='/passwordchangedone/'), name= 'passwordchange'),
    # here success_url= '/passwordchangedone/' means if this link work is successful, then it thould go to passwordchangedone page
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name= 'app/passwordchangedone.html'), name= 'passwordchangedone'),

    path('registration/', views.CustomerRegisterationView.as_view(), name='customerregistration'),
    
    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),

    # there are 4 forms of password-reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name= 'app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name= 'app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'), 
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name= 'app/password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
# static(......) this whole is writted as changes were made in settings.py, and now can store img from admin input