from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# 定义用户注册表单，继承自UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # 添加email字段

    class Meta:
        model = User  # 指定模型为User
        fields = ['username', 'email', 'password1', 'password2']  # 指定表单包含的字段

# 定义用户更新表单，继承自ModelForm
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  # 添加email字段

    class Meta:
        model = User  # 指定模型为User
        fields = ['username', 'email']  # 指定表单包含的字段

# 定义个人资料更新表单，继承自ModelForm
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile  # 指定模型为Profile
        fields = ['avatar', 'piece_color', 'sound_enabled']  # 指定表单包含的字段