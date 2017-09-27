from django.shortcuts import render

def home(request):
	visit=0
	context={"visit":visit}
	return render(request, 'home/home.html',context)


