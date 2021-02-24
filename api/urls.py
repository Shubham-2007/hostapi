
# from django.contrib import admin
# from django.urls import path
# from file_app import views

# urlpatterns = [
#     path('digit/',views.getimagefromrequest)
# ]

from django.conf.urls import url
from .views import getimagefromrequest

urlpatterns = [
    url(r'^digit/', getimagefromrequest.as_view(), ),
]




# https://dashboard.heroku.com/apps
# https://www.codementor.io/@jamesezechukwu/how-to-deploy-django-app-on-heroku-dtsee04d4#audience-assumption
# https://www.youtube.com/watch?v=nGlMa4KRnmA
# https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1
# https://medium.com/free-code-camp/writing-a-killer-software-engineering-resume-b11c91ef699d
##