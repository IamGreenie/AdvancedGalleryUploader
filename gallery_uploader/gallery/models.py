from django.db import models

# Create your models here.
#create a model called image with an image field and a title field
class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    def __str__(self):
        return self.title

class Comment(models.Model):
    image = models.ForeignKey(Image, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.image.title} at {self.created_at}'