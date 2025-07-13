from django.urls import path
from . import views
urlpatterns=[
    path('',views.store,name="store"),
    path('product/<int:product_id>',views.product_page,name="product"),
    path('thankyou',views.say_thankyou,name="thankyou"),
    path('aboutus',views.about_us,name="aboutus"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('super-silvo-login',views.login_view,name="super-silvo-login"),
    path('logout',views.logout_view,name="logout"),
    path('add',views.add_product,name="add"),
    path('zrorders',views.orders,name="zrorders"),
    path('allproduct',views.all_product,name="allproduct"),
    path('allproduct/<int:product_id>',views.edit_product,name="edit_product"),
    # Rest API's
    path('zr/orders',views.zrorders),
    path('products/',views.product_list),
    path('products/<int:product_id>',views.product_detail),
    path('orders',views.order_list),
    path('wilayas',views.wilaya),
    path('wilayas/<int:IDWilaya>',views.get_wilaya)

]