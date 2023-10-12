from django.urls import path
from .views import GotOrderView,GotOrderDetailView,DistributeOrderView,DistributeOrderDetailView,PersonView,PersonDetailView
urlpatterns = [
    path('', GotOrderView.as_view(),name = "add_order" ),
    path('<int:pk>/', GotOrderDetailView.as_view(),name = "detail_order" ),
    path('distribute/', DistributeOrderView.as_view(),name = "dist_order" ),
    path('distribute/<int:pk>/', DistributeOrderDetailView.as_view(),name = "detail_dist_order" ),
    path('person/', PersonView.as_view(),name = "person" ),
    path('person/<int:pk>/', PersonDetailView.as_view(),name = "detail_person" ),
]