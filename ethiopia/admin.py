from django.contrib import admin
from .models import Player,Club,Refree,verificationcode,Stadium,Messagetoclubs,Game,Schedule,Supporter,MesssageFromClubToPlayer,Public_news,Advert,Comment,messageToRefree
from import_export.admin import ImportExportModelAdmin 
# Register your models here.
admin.site.register(verificationcode)
admin.site.register(Stadium)


admin.site.register(Supporter)
admin.site.register(MesssageFromClubToPlayer)
admin.site.register(Public_news)
admin.site.register(Advert)

admin.site.register(messageToRefree)
@admin.register(Player,Club,Refree,Schedule,Game,Messagetoclubs,Comment)

class ViewAdmin(ImportExportModelAdmin):
	pass