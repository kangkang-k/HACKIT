# models.py
from django.utils import timezone
from user.models import *

class Bounty(models.Model):
    STATUS_CHOICES = [
        ('open', '开放中'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('closed', '已关闭'),
    ]

    TYPE_CHOICES = [
        ('bug', '漏洞挖掘'),
        ('development', '功能开发'),
        ('design', '设计任务'),
        ('other', '其他类型'),
    ]

    title = models.CharField('标题', max_length=100)
    description = models.TextField('详细描述')
    reward = models.DecimalField('赏金', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    deadline = models.DateTimeField('截止时间', null=True, blank=True)

    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='open')
    bounty_type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES)

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_bounties',
        verbose_name='创建者'
    )
    solver = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='solved_bounties',
        verbose_name='解决者'
    )

    tech_stack = models.CharField('技术栈', max_length=200, blank=True)
    difficulty = models.PositiveSmallIntegerField('难度等级', default=1)  # 1-5级

    views = models.PositiveIntegerField('浏览次数', default=0)
    favorites = models.PositiveIntegerField('收藏次数', default=0)

    class Meta:
        verbose_name = '悬赏任务'
        verbose_name_plural = '悬赏任务'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} (赏金: {self.reward})"