from django.shortcuts import render,get_object_or_404,redirect
import urllib.request
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm,BuyForm,SellForm
from .models import Transaction,UserInfo,Portfolio
import math

app_name='price'

'''def portfolio(request):
	if not request.user.is_authenticated():
		return render(request, 'price/login.html')
	else:
		display=[]
		company = ["GOOG","AAPL","RELIANCE","ICICIBANK","HCLTECH","WIPRO"]
		for cs in company:
			d=[]
			for t in Transaction.objects.filter(user=request.user,company_symbol=cs):
				purchase_quantity=0
				if t.sale_amount == 0:
					purchase_quantity=t.purchase_amount/t.purchase_rate
					
					
		return render(request,'price/portfolio.html',{'transact':transact})'''
		
def portfolio(request):
	if not request.user.is_authenticated():
		return render(request, 'price/login.html')
	else:
		display=[]
		company = ["GOOG","AAPL","RELIANCE","ICICIBANK","HCLTECH","WIPRO"]
		dict={}
		dict["GOOG"]=304466804484872
		dict["AAPL"]=22144
		dict["RELIANCE"]=4674509
		dict["ICICIBANK"]=16345036
		dict["HCLTECH"]=10627180
		dict["WIPRO"]=9055815
		user_info = UserInfo.objects.get(user=request.user)
		sp=0
		for c in company:
			pf=Portfolio.objects.get(user=request.user,c_name=c)
			pf.bal_shares=pf.bought_shares-pf.sold_shares
			url="https://www.google.com/finance?q=NSE%3A"+c
			htmlfile = urllib.request.urlopen(url)
			htmltext = htmlfile.read().decode('utf-8')
			regex = '<span id="ref_'+str(dict[c])+'_l">(.+?)</span>'
			pattern = re.compile(regex)
			rate = re.findall(pattern,htmltext)
			price=(float(rate[0]))
			pf.current_market_price=price
			pf.market_evaluation=price*pf.bal_shares
			sp+=pf.market_evaluation
			display.append(pf)
			pf.save()
			
		net_profit=sp+user_info.virtual_cash-50000.0
		vc=	user_info.virtual_cash
		name=request.user.username
		context={ "display":display , "net_profit":net_profit, "vc":vc , "name":name }
		return render(request,'price/portfolio.html',context)

		
			
			
		
	
	
def index(request):
	company = ["GOOG","AAPL","RELIANCE","ICICIBANK","HCLTECH","WIPRO"]
	context = {
					"company": company,
				}
	return render(request, 'price/index.html', context)
	
def detail(request,company_symbol):
		dict={}
		dict["GOOG"]=304466804484872
		dict["AAPL"]=22144
		dict["RELIANCE"]=4674509
		dict["ICICIBANK"]=16345036
		dict["HCLTECH"]=10627180
		dict["WIPRO"]=9055815
		url="https://www.google.com/finance?q=NSE%3A"+company_symbol
		htmlfile = urllib.request.urlopen(url)
		htmltext = htmlfile.read().decode('utf-8')
		regex = '<span id="ref_'+str(dict[company_symbol])+'_l">(.+?)</span>'
		pattern = re.compile(regex)
		rate = re.findall(pattern,htmltext)
		price=((float(rate[0]))*100)/100
		context={ "price":price , "company_symbol":company_symbol }
		return render(request,'price/detail.html',context)
		
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'price/login.html', context)


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				company=["GOOG","AAPL","RELIANCE","ICICIBANK","HCLTECH","WIPRO"]
				context = { "company": company,
				}
				return render(request, 'price/index.html', context)
			else:
				return render(request, 'price/login.html', {'error_message': 'Your account has been disabled'})
		else:   
			return render(request, 'price/login.html', {'error_message': 'Invalid login'})
	return render(request, 'price/login.html')


def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		new_user=UserInfo()
		new_user.user=user
		new_user.virtual_cash=50000.0
		#user.save()
		new_user.save()
		company=["GOOG","AAPL","RELIANCE","ICICIBANK","HCLTECH","WIPRO"]
		for c in company:
			pf=Portfolio()
			pf.user=user
			pf.c_name=c
			pf.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				company=["GOOG", "AAPL", "RELIANCE", "ICICIBANK", "HCLTECH", "WIPRO"]
				return render(request, 'price/index.html', {'company':company})
                
	context = {
        "form": form,
               }
	return render(request, 'price/register.html', context)
	
def buy(request,company_symbol,price):
	if not request.user.is_authenticated():
		return render(request, 'price/login.html')
	else:
		#transact = get_object_or_404(Transaction, pk=request.user.id)
		if request.method=="POST":
			form = BuyForm(request.POST)
			if form.is_valid():
				try:
					#transact = get_object_or_404(Transaction, pk=request.user.id)
					pkey=request.user.id
					transact = form.save(commit=False)
					purchase_quantity = int(form.cleaned_data['purchase_quantity'])
					price=float(price)
					user_info = UserInfo.objects.get(user=request.user)
					if user_info.virtual_cash<(price*purchase_quantity):
						return render(request, 'price/buy.html', {'error_message': "You don't have enough virtual cash to buy the shares"})
					elif purchase_quantity == 0:
						return render(request, 'price/sell.html', {'error_message': "Please enter non zero purchase quantity"})				
					else:
						pf=Portfolio.objects.get(user=request.user,c_name=company_symbol)
						pf.bought_shares+=purchase_quantity
						pf.save()
						
						
						transact.user=user_info.user
						user_info.virtual_cash-=price*purchase_quantity
						transact.virtual_cash=user_info.virtual_cash
						user_info.save()
						transact.company_symbol=company_symbol
						transact.purchase_rate = price
						transact.balance_shares=purchase_quantity
					
						#transact.purchase_quantity = quantity
						transact.purchase_amount = price*purchase_quantity
						transact.save()
						
				except Transaction.DoesNotExist:
					return render(request, 'price/buy.html', {'error_message': "Error in retreiving transaction table"})
				return render(request,'price/status.html',{'transact':transact})
		else:
			form = BuyForm()
			return render(request, 'price/buy.html', {'form': form})
			
				
		
def sell(request,cs,price):
	if not request.user.is_authenticated():
		return render(request, 'price/login.html')
	else:
		if request.method=="POST":
			form = SellForm(request.POST)
			if form.is_valid():
				try:
					sale_quantity = int(form.cleaned_data['sale_quantity'])
					transacts = []
					q=0
					purchase_amount=0
					#primary=Transaction.objects.filter(user=request.user)
					
					for t in Transaction.objects.filter(user=request.user,company_symbol=cs,sale_amount=0.0):
						if t.purchase_quantity>0:
							purchase_amount+=t.purchase_rate*t.purchase_quantity
							q+=t.purchase_quantity
							transacts.append(t)
					
					transact=Transaction()
					transact.user=request.user
					if not q>=sale_quantity and sale_quantity>0:
						return render(request, 'price/sell.html', {'error_message': "You don't have shares of this company"})
					elif sale_quantity == 0:
						return render(request, 'price/sell.html', {'error_message': "Please enter non zero sell quantity"})				
					else:
						pf=Portfolio.objects.get(user=request.user,c_name=cs)
						pf.sold_shares+=sale_quantity
						
						
						price=float(price)
						user_info = UserInfo.objects.get(user=request.user)
						transact.purchase_rate=purchase_amount/q
						transact.purchase_rate=(math.ceil(transact.purchase_rate*100)/100)
						pr=purchase_amount/q
						transact.purchase_amount=(transact.purchase_rate)*q
						
						transact.company_symbol=cs
						transact.purchase_quantity=q
						#transact.virtual_cash+=price*quantity
						transact.sale_rate = price
						transact.sale_quantity = sale_quantity
						transact.sale_amount = price*sale_quantity
						transact.balance_shares=q-sale_quantity
						vc=user_info.virtual_cash
						transact.virtual_cash=vc+price*sale_quantity
						user_info.virtual_cash=transact.virtual_cash
						transact.profit=price*sale_quantity-pr*sale_quantity
						pf.profit+=transact.profit
						pf.save()
						transact.save()
						user_info.save()
						context={'transact':transact
						}
						
						for t in transacts:
							if sale_quantity:
								if t.purchase_quantity>sale_quantity:
									t.purchase_quantity-=sale_quantity
									sale_quantity=0
									t.save()
								else:
									t.purchase_quantity=0
									sale_quantity-=1
									t.save()
								
				except Transaction.DoesNotExist:
					return render(request, 'price/sell.html', {'error_message': "Error in retreiving transaction table"})
				return render(request, 'price/status.html', context)
		else:
			form = SellForm()
			return render(request, 'price/sell.html', {'form': form})
		

