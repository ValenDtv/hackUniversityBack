"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MallHelper import views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('register/', views.register),
	path('authInput/', views.authorization),
	path('insertMapInput/', views.create_map),
    path('mapUpdate/', views.update_map),
    path('mapDelete/', views.delete_map),
    path('selectMaps/', views.select_maps),
	path('createPlace/', views.create_place),
    path('updatePlace/', views.update_place),
    path('deletePlace/', views.delete_place),
    path('selectPlaces/', views.select_places),
    path('insertRecomendation/', views.create_rec),
    path('updateRecomendation/', views.update_rec),
	path('deleteRecomendation/', views.delete_rec),
	path('selectRecomendations/', views.select_rec),
    path('selectAllAttributes/', views.select_allAttrs),
    path('addRecomendationAttribute/', views.addRecomendationAttribute),
    path('deleteRecomendationAttribute/', views.deleteRecomendationAttribute),
	path('photoData/', views.analysisPhotoData)	
]
