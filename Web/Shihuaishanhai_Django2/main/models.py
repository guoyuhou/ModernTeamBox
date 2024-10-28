from django.db import models
from django.urls import reverse

class Room(models.Model):
    name = models.CharField('房间名称', max_length=100)
    price = models.DecimalField('价格', max_digits=8, decimal_places=2)
    area = models.CharField('面积', max_length=50)
    bed_type = models.CharField('床型', max_length=50)
    max_guests = models.IntegerField('最大入住人数')
    window = models.BooleanField('是否有窗', default=True)
    smoking = models.BooleanField('是否可吸烟', default=False)
    floor = models.IntegerField('楼层')
    description = models.TextField('描述', blank=True)
    image = models.ImageField('房间图片', upload_to='rooms/', blank=True)
    facilities = models.ManyToManyField('Facility', verbose_name='设施', related_name='rooms')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '房间'
        verbose_name_plural = verbose_name
        ordering = ['price']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:room_detail', kwargs={'pk': self.pk})

class Facility(models.Model):
    CATEGORY_CHOICES = [
        ('basic', '基础设施'),
        ('bathroom', '浴室设施'),
        ('media', '媒体设施'),
        ('other', '其他设施')
    ]
    
    name = models.CharField('设施名称', max_length=100)
    category = models.CharField('设施类别', max_length=50, choices=CATEGORY_CHOICES)
    icon = models.CharField('图标类名', max_length=50, blank=True)
    
    class Meta:
        verbose_name = '设施'
        verbose_name_plural = verbose_name
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.get_category_display()}-{self.name}'

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='房间')
    guest_name = models.CharField('客人姓名', max_length=100)
    phone = models.CharField('电话', max_length=20)
    check_in = models.DateField('入住日期')
    check_out = models.DateField('离店日期')
    special_requests = models.TextField('特殊要求', blank=True, null=True)
    total_price = models.DecimalField('总价', max_digits=10, decimal_places=2)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')  # 新增状态字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '预订'
        verbose_name_plural = '预订'

    def __str__(self):
        return f'{self.guest_name} - {self.room.name}'

class Attraction(models.Model):
    name = models.CharField('景点名称', max_length=100)
    distance = models.DecimalField('距离(公里)', max_digits=5, decimal_places=1)
    rating = models.DecimalField('评分', max_digits=2, decimal_places=1)
    description = models.TextField('描述', blank=True)
    image = models.ImageField('景点图片', upload_to='attractions/')

    class Meta:
        verbose_name = '周边景点'
        verbose_name_plural = verbose_name
        ordering = ['distance']

    def __str__(self):
        return self.name
