from django.urls import path, include
urlpatterns = [
    path('activity/', include('activity.urls')),
    path('appointment/', include('appointment.urls')),
    path('message/', include('message.urls')),
    path('', include('common.urls')),
    path('competition/', include('competition.urls')),
    path('group/', include('group.urls')),
    path('user/', include('user.urls')),
]
