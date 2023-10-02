from django.urls import path
from django.views.generic import TemplateView
from django.urls import path
from Payment import views
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns=[
path('', TemplateView.as_view(template_name='index.html'), name='home'),
path('logout/',views.logout_users,name='logout'),
path('api/payments/', views.PaymentListCreateView.as_view(), name='payment_list_create'),
path('api/payments/<int:pk>/', views.PaymentRetrieveUpdateDeleteView.as_view(), name='payment_retrieve_update_delete'),
path('api/settlements/', views.SettlementListCreateView.as_view(), name='settlement_list_create'),
path('api/settlements/<int:pk>/', views.SettlementRetrieveView.as_view(), name='settlement_retrieve'),
#path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


