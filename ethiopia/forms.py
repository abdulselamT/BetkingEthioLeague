from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Club,Player,Refree,Game,Supporter,MesssageFromClubToPlayer,Comment,verificationcode,Stadium


"""here is our form that we want to deal with databse to update,register,delete"""


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
class ClubForm(ModelForm):
	class Meta:
		model=Club
		fields='__all__'
		exclude=['user','total_goals','result','total_wins','total_lose','total_tight','rank','best_player','total_tie']

class PlayerForm(ModelForm):
	class Meta:
		model=Player
		fields='__all__'
		exclude=['user','goal_scored',"penality","salary","malia_number",'position',"yellow_card_seen","red_card_seen","club_name"]
class SupporterForm(ModelForm):
	class Meta:
		model=Supporter
		field='__all__'
		exclude=['user','club_name']
class RefreeForm(ModelForm):
	class Meta:
		model=Refree
		fields='__all__'
		exclude=['user','salary']
class GameForm(ModelForm):
	class Meta:
		model=Game
		fields=['goal_of_first_club','goal_of_last_club']
class ClubPlayerForm(ModelForm):
	class Meta:
		model=Player
		fields=['position','salary','malia_number']
			
class MesssageFromClubToPlayerForm(ModelForm):
	class Meta:
		model = MesssageFromClubToPlayer
		fields="__all__"
		exclude=["player"]
class CommentForm(ModelForm):
	class Meta:
		model=Comment
		fields="__all__"
		exclude=["to_club"]
class verificationtoplayer(ModelForm):
	class Meta:
		model = verificationcode
		fields=['player_code']
class StadiumForm(ModelForm):
	class Meta:
		model=Stadium
		fields='__all__'

class GameForm(ModelForm):
	class Meta:
		model=Game
		fields=["refre_chosen",'first_club','last_club','playing_date']
