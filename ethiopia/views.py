from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CreateUserForm,RefreeForm,MesssageFromClubToPlayerForm,GameForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms  import ClubForm,PlayerForm,GameForm,ClubPlayerForm,SupporterForm,CommentForm,StadiumForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users
from .models import verificationcode,Messagetoclubs,Game,Club,Player,Schedule,MesssageFromClubToPlayer,Public_news,Advert,Comment,messageToRefree,Supporter,Refree
from django.forms import inlineformset_factory
from.filters import PlayerFilter,GoalFilter
import csv
# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['PLAYER'])

def check_password(a,b):
	if a==b:
		return True
	return False

def PlayerPage(request):
	context={"page":"this is Player page"}
	return render(request,'ethiopia/player.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['CLUB'])
def ClubPage(request):
	name=(request.user.club.club_name)
	players=Player.objects.filter(club_name=name)
	players=players.order_by('-goal_scored')
	specific=Messagetoclubs.objects.filter(club=name)
	general=Messagetoclubs.objects.filter(club="all")
	print(general)
	myFilter=PlayerFilter(request.GET,queryset=players)
	players=myFilter.qs
	context={"page":"this is Club page","news":specific,"generals":general,"players":players,'myFilter':myFilter}
	return render(request,'ethiopia/club.html',context)
def Messagetoplayer(request,pk):
	form=MesssageFromClubToPlayerForm()
	name=Player.objects.get(id=pk)
	name=name.Player_name
	if request.method=="POST":
		form=MesssageFromClubToPlayerForm(request.POST)
		if form.is_valid():
			x=form.save(commit=False)
			x.player=name
			x.save()
			return redirect('/')
	context={'form':form}
	return render(request,'ethiopia/messagefromclub.html',context)
def ScoreBoard(request):
	table=Club.objects.order_by('-result','-total_goals')
	context={"page":"this is ScoreBoard page","table":table}
	return render(request,'ethiopia/scoreboard.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['REFREE'])
def RefreePage(request):
	x=request.user.refree.refree_name
	
	try:
		y=Game.objects.filter(refre_chosen=x).last()

		first_club=Club.objects.get(club_name=y.first_club)
		last_club=Club.objects.get(club_name=y.last_club)
		page="THIS IS ADDING TO PLAYER PAGE"
		refreename=request.user.refree.refree_name
		games=Game.objects.filter(refre_chosen=refreename).last()
		club1=games.first_club
		club2=games.last_club
		players=Player.objects.all()
		myFilter=GoalFilter(request.GET,queryset=players)
		players=myFilter.qs
		if request.method=="POST":
			first_goal=int(request.POST['first_club_goal'])
			last_goal=int(request.POST['last_club_goal'])
			if first_goal==last_goal:
				first_club.result+=1
				first_club.total_tie+=1
				last_club.total_tie+=1
				last_club.result+=1
			elif first_goal>last_goal:
				first_club.result+=3
				first_club.total_wins+=1
				last_club.total_lose+=1
			else:
				last_club.result+=3
				last_club.total_wins+=1
				first_club.total_lose+=1
			first_club.total_goals+=first_goal
			last_club.total_goals+=last_goal
			first_club.save()
			last_club.save()
			y.save()
			return redirect('home')
	except:
		return HttpResponse("no active game")
		
	return render(request,'ethiopia/refree.html',{"form":y,"players":players,"myFilter":myFilter})
@login_required(login_url='login')
def CommentPage(request):
	form=CommentForm()
	club_list = Club.objects.all()
	if request.method=="POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			x=form.save()
			x.to_club=request.POST['clubs']
			print(x.to_club)
			x.save()
			return redirect('home')
	context={"page":"this is commentPage","forms":form,'club_list':club_list}
	return render(request,'ethiopia/comment.html',context)

def HomePage(request):
	topscorer=Player.objects.order_by('-goal_scored')
	context={"page":"this is home page"}
	public=Public_news.objects.all().order_by('-date_created')
	name=request.user.username
	print(name)
	specific=""
	general=""
	advert=""
	schedules=Schedule.objects.all().order_by('-playing_date')
	fill="";
	comment=""
	set_game=""

	if name:
		name=name
		ide=request.user.id
		group = request.user.groups.all()[0].name
		group=group.lower()
		try:
			y=request.user.groups.all()[1].name
			set_game='set_game'
		except:
			pass

		
			
		if group=='club':
			name=request.user.club.club_name
			advert=Comment.objects.filter(to_club=name).order_by('-date_created')
			group="club/"
		
		elif group=='player':
			players=request.user.player.Player_name
			specific=MesssageFromClubToPlayer.objects.filter(player=players)
			general=MesssageFromClubToPlayer.objects.filter(player="all")
			group="updateplayer/"+str(ide)
		elif group=='supporter':
			advert=Advert.objects.all().order_by('-date_created')
			comment="comment"
			group="updatesupporter/"+str(ide)

		else:
			name=request.user.refree.refree_name
			group="updaterefree/"+str(ide)
			fill="Fill POINTS"
			players=request.user.refree.refree_name
			specific=messageToRefree.objects.filter(refree=players)
			general=messageToRefree.objects.filter(refree="all")
		

	else:
		name="login"
		group="login"
		advert=Advert.objects.all().order_by('-date_created')
	playercode=verificationcode.objects.last().player_code
	context={"page":"this is home page","p":playercode,'name':name,'group':group,"schedules":schedules,"fill":fill,"specific":specific,"general":general,"public":public,"advert":advert,"comment":comment,'set_game':set_game,'top_goal_scorer':topscorer}
	return render(request,'ethiopia/home.html',context)
@unauthenticated_user
def RegsterRefree(request):
	refreecode=verificationcode.objects.last().refree_code
	form = CreateUserForm()
	refreeform=RefreeForm()
	if request.method == 'POST':
		user_input=request.POST['check']
		if user_input==refreecode:
			form = CreateUserForm(request.POST,request.FILES)
			refreeform=RefreeForm(request.POST)
			if form.is_valid() and refreeform.is_valid():
				
				username = form.cleaned_data.get('username')
				refreeform=refreeform.save(commit=False)
				group = Group.objects.get(name='REFREE')
				user.groups.add(group)
				refreeform.user=user
				refreeform.save()
				messages.success(request, 'Account was created for ' + username)
				return redirect('login')
		else:
			return render(request,'ethiopia/registerplayer.html',{"error":"you are not allowed"})	

	context = {'forms':form,"refreeform":refreeform}
	return render(request, 'ethiopia/registerrefree.html', context)
@unauthenticated_user
def RegisterPlayer(request):
	playercode=verificationcode.objects.last().player_code
	club_list = Club.objects.all()
	print(club_list)
	form = CreateUserForm()
	playerform=PlayerForm()
	if request.method == 'POST':
		user_input=request.POST['check']
		if user_input==playercode:
			form = CreateUserForm(request.POST)
			playerform=PlayerForm(request.POST,request.FILES)
			if form.is_valid() and playerform.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				playerform=playerform.save(commit=False)
				group = Group.objects.get(name='PLAYER')
				user.groups.add(group)
				playerform.user=user
				playerform.save()
				x=Player.objects.last()
				x.club_name=request.POST['clubs']
				print(x.club_name)
				x.save()
				messages.success(request, 'Account was created for ' + username)

				return redirect('login')
			
		else:
			return render(request,'ethiopia/registerplayer.html',{"error":"you are not allowed"})

	context = {'forms':form,"playerform":playerform,'club_list':club_list}
	return render(request, 'ethiopia/registerplayer.html', context)
@unauthenticated_user
def RegisterClub(request):
	clubcode=verificationcode.objects.last().club_code
	form = CreateUserForm()
	clubform=ClubForm()
	if request.method == 'POST':
		user_input=request.POST['check']
		if user_input==clubcode:
			form = CreateUserForm(request.POST)
			clubform=ClubForm(request.POST,request.FILES)
			if form.is_valid() and clubform.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				clubform=clubform.save(commit=False)
				group = Group.objects.get(name='CLUB')
				user.groups.add(group)
				clubform.user=user
				clubform.save()
				messages.success(request, 'Account was created for ' + username)

				return redirect('login')
		else:
			return render(request,'ethiopia/registerclub.html',{"error":"you are not allowed"})	

	context = {'forms':form,"clubform":clubform}
	return render(request, 'ethiopia/registerclub.html', context)
@unauthenticated_user
def RegisterSupporter(request):
	form = CreateUserForm()
	supporterform=SupporterForm()
	club_list = Club.objects.all()
	print(1)
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		supporterform=SupporterForm(request.POST,request.FILES)
		print(2)
		if form.is_valid() and supporterform.is_valid():
			print(3)
			user = form.save()
			username = form.cleaned_data.get('username')
			supporterform=supporterform.save(commit=False)
			group = Group.objects.get(name='SUPPORTER')
			user.groups.add(group)
			supporterform.user=user
			x=supporterform.save()

			x=Supporter.objects.last()
			x.club_name=request.POST['clubs']
			print(x.club_name)
			x.save()
			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
			
		
	context = {'forms':form,"supporterform":supporterform,'club_list':club_list}
	return render(request, 'ethiopia/registersupporter.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['CLUB'])
def RegisterStadium(request):
	forms=StadiumForm()
	if request.method=="POST":
		forms=StadiumForm(request.POST)
		if forms.is_valid():
			forms.save()
			return redirect('club')
	context={"page":"This is RegisterStadium page","forms":forms}
	return render(request,'ethiopia/registerstadium.html',context)

@login_required(login_url='login')
def UpdatePlayer(request,pk):
	user=User.objects.get(id=pk)
	form=PlayerForm(instance=user.player)
	if request.method=="POST":
		form=PlayerForm(request.POST,request.FILES,instance=user.player)
		if form.is_valid():
			form.save()
			return redirect("home")
	context={"page":"This is UpdateplayerPage","forms":form}
	return render(request,'ethiopia/updateplayer.html',context)
@login_required(login_url='login')
def UpdateClub(request,pk):
	user=User.objects.get(id=pk)
	form=ClubForm(instance=user.club)
	if request.method=="POST":
		form=ClubForm(request.POST,request.FILES,instance=user.club)
		if form.is_valid():
			form.save()
			return redirect("club")
	context={"page":"This is UpdateplayerPage","forms":form}
	return render(request,'ethiopia/updateclub.html',context)
@login_required(login_url='login')
def UpdateRefree(request,pk):
	user=User.objects.get(id=pk)
	form=RefreeForm(instance=user.refree)
	if request.method=="POST":
		form=RefreeForm(request.POST,request.FILES,instance=user.refree)
		if form.is_valid():
			form.save()
			return redirect("home")
	context={"page":"This is UpdateClubPage","forms":form}
	return render(request,'ethiopia/updaterefree.html',context)
@login_required(login_url='login')
def UpdateSupporter(request,pk):
	user=User.objects.get(id=pk)
	form=SupporterForm(instance=user.supporter)
	if request.method=="POST":
		form=SupporterForm(request.POST,request.FILES,instance=user.supporter)
		if form.is_valid():
			form.save()
			return redirect("/")
	context={"page":"This is UpdateplayerPage","forms":form}
	return render(request,'ethiopia/updatesupporter.html',context)
@login_required(login_url='login')
def UpdateStadium(request):
	context={"page":"This is UpdateStadiumPage"}
	return render(request,'ethiopia/updatestadium.html',context)
def UpdatePlayerClub(request,pk):
	order = Player.objects.get(id=pk)
	form = ClubPlayerForm(instance=order)
	if request.method == 'POST':
		form =ClubPlayerForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('club')

	context = {'forms':form}
	return render(request, 'ethiopia/updateplayerclub.html', context)
def RemovePlayerClub(request,pk):
	remoplayer = Player.objects.get(id=pk)
	if request.method=="POST":
		remoplayer.delete()
		return redirect('/')
	context={'remoplayer':remoplayer}
	return render(request,'ethiopia/removeplayerclub.html',context)
@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('user_name')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
				group=group.lower()
			return redirect("/")
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'ethiopia/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')
def VerificationToclub(request):
	page="this is where you put verification player_code"
	y=verificationcode.objects.last()
	if request.method=="POST":
		x=request.POST['verificationtoplayer']
		y.player_code=x
		y.save()
	context={"page":page}
	return render(request,'ethiopia/verification.html',context)
def addgoaltoplayer(request,pk):
	page="THIS IS ADDING TO PLAYER PAGE"
	player=Player.objects.get(id=pk)
	if request.method=="POST":
		x=request.POST['done']
		player.goal_scored+=int(x)
		player.save()
	context={"page":page,"player":player}
	return render(request,"ethiopia/goaltoplayer.html",context)



def best_discipleaned(request):
	best_player_list=Player.objects.order_by('-red_card_seen','-yellow_card_seen')
	topscorer=Player.objects.order_by('-goal_scored')
	print(best_player_list)
	context={'b':best_player_list,"top":topscorer}
	return render(request,"ethiopia/disciplean.html",context)
@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def game(request):
	refrees=Refree.objects.all()
	clubs=Club.objects.all()
	
	if request.method=="POST":
		first_club=request.POST['first_club']
		last_club=request.POST['last_club']
		refre_chosen=request.POST['refree_chosen']
		playing_date=request.POST['playing_date']
		Game.objects.create(first_club=first_club,last_club=last_club,refre_chosen=refre_chosen, playing_date=playing_date)
	context={'refrees':refrees,'clubs':clubs}
	return render(request,"ethiopia/game.html",context)



