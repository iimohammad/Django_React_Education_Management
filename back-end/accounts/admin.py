from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from .models import Teacher, Student, EducationalAssistant, User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_number', 'gender', 'phone', 'is_staff')
    list_filter = ('gender', 'birthday', 'is_active', 'is_staff')
    sortable_by = ('username', 'user_number')
    list_editable = ('is_staff',)
    readonly_fields = ('user_number',)
    ordering = ('date_joined',)
    search_fields = ('username', 'email', 'user_number', 'phone')
    search_help_text = "Search in: Username, Email, User Number, Phone"
    # list_display_links = ('username', 'user_number')
    # date_hierarchy = 'birthday'
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'user_number', 'national_code',
                                      'birthday', 'profile_image', 'phone', 'address', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    actions = ['set_gender_male', 'set_gender_female', 'delete_inactive_users']

    def set_gender_male(self, request, queryset):
        queryset.update(gender="M")
    set_gender_male.short_description = "Set selected users' gender as male"

    def set_gender_female(self, request, queryset):
        queryset.update(gender="F")
    set_gender_female.short_description = "Set selected users' gender as female"

    def delete_inactive_users(self, request, queryset):
        three_months_ago = timezone.now() - timezone.timedelta(days=90)
        inactive_users = queryset.filter(last_login__lt=three_months_ago)
        deleted_count, _ = inactive_users.delete()
        self.message_user(request, f"{deleted_count} inactive users deleted.")
    delete_inactive_users.short_description = "Delete inactive users (3 months)"

admin.site.register(User, CustomUserAdmin)


admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(EducationalAssistant)
