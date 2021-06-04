import django_filters
from .models import *
""" this is for filter """
class PlayerFilter(django_filters.FilterSet):
	class Meta:
		model=Player
		fields=['Player_name','goal_scored','malia_number']

class GoalFilter(django_filters.FilterSet):
	class Meta:
		model=Player
		fields=['club_name','malia_number']

		