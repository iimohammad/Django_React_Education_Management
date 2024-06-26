from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.html import format_html
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.auth.forms import UserCreationForm
import os
admin_url = os.environ.get('Admin')
from accounts.resource import (UserResource,
                               TeacherResource,
                               StudentResource,
                               EducationalAssistantResource)

from .models import AdminUser, EducationalAssistant, Student, Teacher, User
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomUserAdmin(UserAdmin, ImportExportActionModelAdmin):
    add_form = CustomUserCreationForm  # Use the custom creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    list_display = ('id', 'username', 'email', 'user_number',
                    'gender', 'phone', 'is_staff')
    list_filter = ('gender', 'birthday', 'is_active', 'is_staff')
    sortable_by = ('username', 'user_number')
    list_editable = ('is_staff',)
    # readonly_fields = ('user_number',)
    ordering = ('date_joined',)
    search_fields = ('username', 'email', 'user_number', 'phone')
    search_help_text = "Search in: Username, Email, User Number, Phone"
    resource_class = UserResource
    # list_display_links = ('username', 'user_number')
    # date_hierarchy = 'birthday'
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'user_number', 'national_code',
                                      'birthday', 'profile_image', 'phone', 'address', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
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


class TeacherAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user_link', 'expertise', 'rank', 'department_link', 'can_be_advisor')
    list_filter = ('rank', 'can_be_advisor')
    sortable_by = ('user',)
    list_editable = ('rank', 'can_be_advisor')
    # readonly_fields = ('expertise',)
    ordering = ('user',)
    search_fields = ('user', 'expertise', 'department')
    search_help_text = "Search in: Username, Expertise, Department"
    list_display_links = ('id', 'user_link', 'department_link')
    resource_class = TeacherResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    actions = ['set_rank_ins', 'set_rank_asp',
               'set_rank_acp', 'set_rank_prof', 'promote_prof_rank']

    def set_rank_ins(self, request, queryset):
        queryset.update(rank="I")
    set_rank_ins.short_description = "Set selected professors' rank as instructor"

    def set_rank_asp(self, request, queryset):
        queryset.update(rank="ASP")
    set_rank_asp.short_description = "Set selected professors' rank as assistant professor"

    def set_rank_acp(self, request, queryset):
        queryset.update(rank="ACP")
    set_rank_acp.short_description = "Set selected professors' rank as associate professor"

    def set_rank_prof(self, request, queryset):
        queryset.update(rank="P")
    set_rank_prof.short_description = "Set selected professors' rank as professor"

    def promote_prof_rank(self, request, queryset):
        for professor in queryset:
            if professor.rank == Teacher.Rank.INSTRUCTOR:
                professor.rank = Teacher.Rank.ASSISTANT_PROF
            elif professor.rank == Teacher.Rank.ASSISTANT_PROF:
                professor.rank = Teacher.Rank.ASSOCIATE_PROF
            elif professor.rank == Teacher.Rank.ASSOCIATE_PROF:
                professor.rank = Teacher.Rank.PROFESSOR
            professor.save()

        self.message_user(
            request, f"Selected professors promoted successfully.")

    promote_prof_rank.short_description = "Promote selected professors"

    def user_link(self, obj):
        user_id = obj.user.id
        user_url = f"http://127.0.0.1:8000/{admin_url}accounts/user/{user_id}/change/"
        return format_html('<a href="{}">{}</a>', user_url, obj.user)

    def department_link(self, obj):
        department_id = obj.department.id
        department_url = f"http://127.0.0.1:8000/{admin_url}education/department/{department_id}/change/"
        return format_html('<a href="{}">{}</a>',
                           department_url, obj.department)

    user_link.short_description = "User"
    department_link.short_description = "Department"


admin.site.register(Teacher, TeacherAdmin)


class StudentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user_link', 'major_link', 'entry_year',
                    'entry_semester', 'gpa', 'military_service_status')
    list_filter = ('major', 'entry_year', 'military_service_status')
    sortable_by = ('user', 'entry_year', 'gpa')
    list_editable = ('military_service_status',)
    # readonly_fields = ('gpa',)
    ordering = ('entry_year',)
    search_fields = ('user', 'entry_semester')
    search_help_text = "Search in: Username, Entry Semester"
    list_display_links = ('id', 'user_link', 'major_link')
    resource_class = StudentResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    def user_link(self, obj):
        user_id = obj.user.id
        user_url = f"http://127.0.0.1:8000/{admin_url}accounts/user/{user_id}/change/"
        return format_html('<a href="{}">{}</a>', user_url, obj.user)

    def major_link(self, obj):
        major_id = obj.major.id
        major_url = f"http://127.0.0.1:8000/{admin_url}education/major/{major_id}/change/"
        return format_html('<a href="{}">{}</a>', major_url, obj.major)

    user_link.short_description = "User"
    major_link.short_description = "Major"


admin.site.register(Student, StudentAdmin)


class EducationalAssistantAdmin(
        ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user_link', 'field_link')
    list_filter = ('field',)
    sortable_by = ('user',)
    ordering = ('user',)
    search_fields = ('field',)
    search_help_text = "Search in: Field"
    list_display_links = ('id', 'user_link', 'field_link')
    resource_class = EducationalAssistantResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    def user_link(self, obj):
        user_id = obj.user.id
        user_url = f"http://127.0.0.1:8000/{admin_url}accounts/user/{user_id}/change/"
        return format_html('<a href="{}">{}</a>', user_url, obj.user)

    def field_link(self, obj):
        field_id = obj.field.id
        field_url = f"http://127.0.0.1:8000/{admin_url}education/major/{field_id}/change/"
        return format_html('<a href="{}">{}</a>', field_url, obj.field)

    user_link.short_description = "User"
    field_link.short_description = "Field"


admin.site.register(EducationalAssistant, EducationalAssistantAdmin)
admin.site.register(AdminUser)
