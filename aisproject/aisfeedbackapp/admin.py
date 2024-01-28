from django.contrib import admin
from .models import ClientData,ClientFeedback

class DataAdmin(admin.ModelAdmin):
    list_display=['fullName','email_id','mobile','address','password']
admin.site.register(ClientData,DataAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display =["Name","Concern","Help","YourFeedback"]
admin.site.register(ClientFeedback, FeedbackAdmin)
