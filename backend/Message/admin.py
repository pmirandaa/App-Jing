from django.contrib import admin

from Message.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sent_date', 'sender', 'reciever', 'subject', 'is_read', 'deleted')
    search_fields = ('sender__name', 'reciever__name', 'subject')

    def sent_date(self, obj):
        return obj.date.strftime("%d/%m/%Y %H:%M")

    sent_date.admin_order_field = 'timefield'

admin.site.register(Message, MessageAdmin)
