from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import re
import bcrypt
from datetime import date 


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

def index(request):
	return render(request,"belt_app/index.html")


def register(request):
	if request.method == 'POST':
		x = False
		if not EMAIL_REGEX.match(request.POST['email']):
			messages.info(request, ' Invalid email ')
			x = True
			# return redirect('/')
		if not NAME_REGEX.match(request.POST['first_name']):
			messages.info(request, ' Invalid name ')
			x = True
			# return redirect('/')
		if not NAME_REGEX.match(request.POST['last_name']):
			messages.info(request, ' Invalid name ')
			x = True
			# return redirect('/')
		if len(request.POST['password']) < 8:
			messages.info(request,'Password must be atleast 8 characters long')
			x = True
			# return redirect('/')
		elif request.POST['password'] != request.POST['confirm_password']:
			messages.info(request,'Password and confirm password are not matched')
			x = True
			# return redirect('/')

		if x:
			return redirect('/')

		else:
			email= request.POST['email']
			password = request.POST['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email = request.POST['email'],password=hashed )
			print ('**************')
	user = User.objects.get(email = email)
	request.session['first_name'] = request.POST['first_name']
	request.session['id'] = user.id
	return redirect('/success')

def success(request):

	friends_list = []
	user = User.objects.get(id=request.session['id'])
	friends = user.friend.all()
	
	for frnd in friends:
		friends_list.append(frnd)

	non_friends = User.objects.all().exclude(id=user.id)
	for frnd in friends_list:
		non_friends = non_friends.exclude(id=frnd.id)
	context = {
		'friends': friends,
		'nonfriends': non_friends,
		}
	return render(request, 'belt_app/success.html', context)


def login(request):
	email = request.POST['email']
	password = request.POST['password']
	x = False;

	if len(email) == 0:
		messages.error(request, "email is required")
		x = True;

	elif not User.objects.filter(email = email).exists():
		messages.error(request, "email is not in the database")
		x=True;

	if x:
		return redirect('/')
	else:
		password = password.encode()
		user = User.objects.get(email = email)
		ps_hashed = user.password
		ps_hashed = ps_hashed.encode()
		request.session['first_name'] = user.first_name
		if bcrypt.hashpw(password, ps_hashed) == ps_hashed:
			request.session['id'] = user.id
			request.session['first_name'] = user.first_name
			return redirect('/success')
		else:
			messages.error(request, "email or password does not match")
			return redirect('/')

def add_friend(request,id):
	new_friend = User.objects.get(id=id)
	user = User.objects.get(id=request.session['id'])
	user.friend.add(new_friend)
	user.save()
	new_friend.friend.add(user)
	

	return redirect('/success')

def show_friend(request,id):
	user = User.objects.get(id=id)
	context={
		'first_name': user.first_name, 
		'last_name':user.last_name,
		'email':user.email,
		
			}
	
	return render(request,"belt_app/show.html",context)

def remove_friend(request,id):
	delete_friend = User.objects.get(id=id)
	user = User.objects.get(id=request.session['id'])
	user.friend.remove(delete_friend)
	user.save()
	delete_friend.friend.remove(user)

	return redirect('/success')


