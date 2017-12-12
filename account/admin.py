from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from account.models import BankAccount, Department, UnlockRecord, User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'name', 'department', 'email', 'kind')

    def clean_password_confirm(self):
        # Check password
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords don\'t match')
        return password_confirm

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'name', 'department', 'email', 'kind', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # Display user model.
    list_display = ('username', 'name', 'kind', 'department', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ( 'name', 'kind', 'department')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'password_confirm', 'name', 'department', 'email', 'kind')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

admin.site.unregister(Group)

admin.site.register(User, UserAdmin)

admin.site.register(BankAccount)
admin.site.register(Department)
admin.site.register(UnlockRecord)
