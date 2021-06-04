from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Club(models.Model):
	user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	club_name=models.CharField(max_length=15)
	logo=models.ImageField(null=True,default="profile1.png")
	total_goals=models.IntegerField(default=0)
	result=models.IntegerField(default=0)
	total_wins=models.IntegerField(default=0)
	total_lose=models.IntegerField(default=0)
	total_tie = models.IntegerField(default=0)
	rank=models.IntegerField(default=1)
	best_player=models.CharField(max_length=15,null=True,blank=True)
	capital = models.CharField(max_length=30,null=True,blank=True)
	def __str__(self):
		return self.club_name
class Supporter(models.Model):
	user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	supporter_name=models.CharField(max_length=15)
	club_name=models.CharField(max_length=200, null=True)
	propic=models.ImageField(null=True,default="profile1.png")
	def __str__(self):
		return self.supporter_name

class Player(models.Model):
	

	user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	club_name=models.CharField(max_length=200, null=True)
	Player_name =models.CharField(max_length=15)
	propic=models.ImageField(null=True,default="profile1.png")
	birth_date=models.DateTimeField()
	birth_place=models.CharField(max_length=15)
	height=models.DecimalField(decimal_places=3,max_digits=5)
	weight_in_newton = models.DecimalField(decimal_places=3,max_digits=5)
	goal_scored = models.IntegerField(default=0)
	yellow_card_seen = models.IntegerField(default=0)
	red_card_seen = models.IntegerField(default=0)
	salary= models.DecimalField(decimal_places=3,max_digits=5,default=0)
	malia_number =models.IntegerField(default=-1)
	position = models.CharField(max_length=15)
	def __str__(self):
		return self.user.username

class verificationcode(models.Model):
	code_giver=models.CharField(max_length=10,null=True,blank=True)
	player_code=models.CharField(max_length=10)
	club_code= models.CharField(max_length=10)
	refree_code=models.CharField(max_length=10)
	def __str__(self):
		return self.code_giver

class Refree(models.Model):
	user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	refree_name =models.CharField(max_length=15)
	propic=models.ImageField(null=True,default="profile1.png")
	birth_place=models.CharField(max_length=15)
	birth_date=models.DateTimeField()
	salary= models.DecimalField(decimal_places=3,max_digits=5,default=0)
	def __str__(self):
		return self.user.username

class Stadium(models.Model):
	club=models.ForeignKey(Club,on_delete=models.CASCADE)
	stadium_name=models.CharField(max_length=15)
	propic=models.ImageField(null=True,default="profile1.png")
	entry_birr = models.DecimalField(decimal_places=3,max_digits=5)
	max_capacity=models.IntegerField()
	description = models.TextField()
	def __str__(self):
		return self.stadium_name
class Messagetoclubs(models.Model):
	
	title=models.CharField(max_length=50)
	message=models.TextField()
	club=models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	dead_line = models.DateTimeField()
	def __str__(self):
		return self.title

class Game(models.Model):
	
	refre_chosen=models.CharField(max_length=15)
	first_club=models.CharField(max_length=15)
	last_club=models.CharField(max_length=15)
	goal_of_first_club=models.IntegerField(null=True,blank=True)
	goal_of_last_club = models.IntegerField(null=True,blank=True)
	playing_date= models.DateTimeField(null=True,blank=True)
	def __str__(self):
		return self.first_club +" VS " + self.last_club

class Schedule(models.Model):
	first_club=models.CharField(max_length=15)
	last_club=models.CharField(max_length=15)
	stadium_name=models.CharField(max_length=15)
	playing_date= models.DateTimeField(null=True)
	def __str__(self):
		return self.first_club +" VS " + self.last_club

class MesssageFromClubToPlayer(models.Model):
	
	title=models.CharField(max_length=50)
	message=models.TextField()
	player=models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	dead_line = models.DateTimeField()
	def __str__(self):
		return self.title


class Public_news(models.Model):
	title=models.CharField(max_length=50)
	message=models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.title

class Advert(models.Model):
	title=models.CharField(max_length=50)
	image=models.ImageField(null=True,default="profile1.png")
	advert_text=models.TextField(null=True,blank=True)
	price_in_dollar=models.IntegerField(default=0)
	advertizer_name=models.CharField(max_length=50,null=True)
	advertizer_Email=models.EmailField(null=True,blank=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	def __str__(self):
		return self.title
	
class Comment(models.Model):
	to_club=models.CharField(max_length=15)
	comment=models.TextField()
	date_created=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	def __str__(self):
		return self.to_club


class messageToRefree(models.Model):
	title=models.CharField(max_length=50)
	message=models.TextField()
	refree=models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	dead_line = models.DateTimeField()
	def __str__(self):
		return self.title





















