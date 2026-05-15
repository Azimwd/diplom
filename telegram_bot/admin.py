# # admin.py

# from django.contrib import admin
# from django.utils.html import format_html
# from django.utils import timezone

# from .models import TelegramProfile


# @admin.register(TelegramProfile)
# class TelegramProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "user",
#         "telegram_id",
#         "chat_id",
#         "username",
#         "created_at",
#     )

#     search_fields = (
#         "user__email",
#         "user__username",
#         "telegram_id",
#         "chat_id",
#         "username",
#     )

#     readonly_fields = (
#         "created_at",
#     )

#     ordering = (
#         "-created_at",
#     )

#     list_select_related = (
#         "user",
#     )

#     fieldsets = (
#         (
#             "Пользователь",
#             {
#                 "fields": (
#                     "user",
#                 )
#             }
#         ),
#         (
#             "Telegram данные",
#             {
#                 "fields": (
#                     "telegram_id",
#                     "chat_id",
#                     "username",
#                 )
#             }
#         ),
#         (
#             "Служебная информация",
#             {
#                 "fields": (
#                     "created_at",
#                 )
#             }
#         ),
#     )


# @admin.register(TelegramLinkCode)
# class TelegramLinkCodeAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "user",
#         "code",
#         "code_status",
#         "expires_at",
#     )

#     list_filter = (
#         "expires_at",
#     )

#     search_fields = (
#         "user__email",
#         "user__username",
#         "code",
#     )

#     ordering = (
#         "-expires_at",
#     )

#     list_select_related = (
#         "user",
#     )

#     readonly_fields = (
#         "code_status",
#     )

#     fieldsets = (
#         (
#             "Пользователь",
#             {
#                 "fields": (
#                     "user",
#                 )
#             }
#         ),
#         (
#             "Код привязки",
#             {
#                 "fields": (
#                     "code",
#                     "code_status",
#                     "expires_at",
#                 )
#             }
#         ),
#     )

#     def code_status(self, obj):
#         if obj.is_expired():
#             return format_html(
#                 "<span style='color: red; font-weight: bold;'>Истёк</span>"
#             )

#         return format_html(
#             "<span style='color: green; font-weight: bold;'>Активен</span>"
#         )

#     code_status.short_description = "Статус"