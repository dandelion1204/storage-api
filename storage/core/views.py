from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')  # 渲染主頁模板