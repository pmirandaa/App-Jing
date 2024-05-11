from django.contrib import admin

from Message.models import Message, Chat, ChatPerson


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sent_date', 'sender', 'chat', 'subject', 'is_read', 'deleted')
    search_fields = ('sender__name', 'chat__name', 'subject')

    def sent_date(self, obj):
        return obj.date.strftime("%d/%m/%Y %H:%M")

    sent_date.admin_order_field = 'timefield'

class ChatAdmin(admin.ModelAdmin):
    list_display= ('name', 'event', 'is_active')
    search_fields= ('name', 'event', 'is_active')

    def Name(self, obj):
        return f'{obj.name}'
    
class ChatPersonAdmin(admin.ModelAdmin):
    list_display= ('person', 'chat')
    search_fields= ('person', 'chat')

admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatPerson, ChatPersonAdmin)
