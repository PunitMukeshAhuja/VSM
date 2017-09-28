from django.shortcuts import render

def home(request):
	if request.user.is_authenticated():
		return render(request, 'price/home2.html')
	else:
		return render(request, 'price/home3.html')


