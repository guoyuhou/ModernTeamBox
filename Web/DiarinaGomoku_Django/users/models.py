from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 定义Profile模型，用于存储用户的个人信息
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 与User模型建立一对一关系
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')  # 用户头像
    wins = models.IntegerField(default=0)  # 胜利次数
    losses = models.IntegerField(default=0)  # 失败次数
    draws = models.IntegerField(default=0)  # 平局次数
    piece_color = models.CharField(max_length=10, choices=[('black', '黑色'), ('white', '白色')], default='black')  # 棋子颜色
    sound_enabled = models.BooleanField(default=True)  # 声音是否启用
    is_online = models.BooleanField(default=False)  # 在线状态

    def __str__(self):
        return f"{self.user.username}的个人资料"  # 返回用户的个人资料字符串

# 当User模型的实例被保存时，自动创建或更新对应的Profile实例
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # 如果是新创建的用户，则创建对应的Profile实例

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # 当用户实例被保存时，保存对应的Profile实例
