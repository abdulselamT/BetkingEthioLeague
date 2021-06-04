from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns =[
path('discipleaned_player',views.best_discipleaned,name='disciplened'),
path('',views.HomePage,name="home"),
path('logout/',views.logoutUser,name="logout"),
path('login/',views.loginPage,name="login"),
path('refree/',views.RefreePage,name="refree"),
path('club/',views.ClubPage,name="club"),
path('comment/',views.CommentPage,name="comment"),
path('registerrefree/',views.RegsterRefree,name="registerrefree"),
path('registerplayer/',views.RegisterPlayer,name="registerplayer"),
path('registerclub/',views.RegisterClub,name="registerclub"),
path('registersupporter/',views.RegisterSupporter,name="registersupporter"),
path('club/registerstadium/',views.RegisterStadium,name="registerstadium"),
path('updateplayer/<str:pk>/',views.UpdatePlayer,name="updateplayer"),
path('updateclub/<str:pk>/',views.UpdateClub,name="updateclub"),
path('updaterefree/<str:pk>/',views.UpdateRefree,name="updaterefree"),
path('updatesupporter/<str:pk>',views.UpdateSupporter,name="updatesupporter"),
path('updatestadium/',views.UpdateStadium,name="updatestadium"),
path('scoreboard/',views.ScoreBoard,name="scoreboard"),
path('club/updateplayerclub/<str:pk>/',views.UpdatePlayerClub,name="updateplayerclub"),
path('club/removeplayerclub/<str:pk>/',views.RemovePlayerClub,name="removeplayerclub"),
path('club/messagetoplayer/<str:pk>/',views.Messagetoplayer,name="messagetoplayer"),
path('club/verification_code/',views.VerificationToclub,name="Verification"),
path('refree/goaltoplayer/<str:pk>/',views.addgoaltoplayer,name="goaltoplayer"),
path('game/',views.game,name="game"),
 path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="ethiopia/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="ethiopia/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="ethiopia/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="ethiopia/password_reset_done.html"), 
        name="password_reset_complete"),

]