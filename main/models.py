from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from main.tasks import notify_user_task


class Created(models.Model):
    """
    нужен для того чтобы во всех моделях не прописывать одно и тоже поле,
    все последующие модели будут наследоваться от этого класса и будут принимать его поля
    """
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        для того чтобы сделать модельку абстрактной
        """
        abstract = True


class Problem(Created):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='problems')

    def __str__(self):
        return f"{self.title}"


class Image(Created):
    image = models.ImageField(upload_to='images')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"{str(self.image)}"


class Reply(Created):
    text = models.TextField()
    image = models.ImageField(upload_to='reply_images')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{str(self.text)[:10]} + ..."


class Comment(Created):
    text = models.TextField()
    author = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name='comments')
    reply_comment = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.text}"


@receiver(post_save, sender=Problem)
def notify_user(sender, instance, created, **kwargs):
    if created:
        email = instance.author.email
        notify_user_task.delay(email)
