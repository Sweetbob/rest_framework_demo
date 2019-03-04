from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class LoginView(View):

    # def dispatch(self, request, *args, **kwargs):
    #     #     super(LoginView, self).dispatch(request, *args, **kwargs)
    #     #     return HttpResponse("自己写的dispatch")

    def get(self, request):
        print("get method")
        return render(request, "login.html")

    def post(self, request):
        print("post method")
        return HttpResponse("ok")
