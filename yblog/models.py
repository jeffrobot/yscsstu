from django.db import models
from django.conf import settings
from django.utils import timezone
from multiselectfield import MultiSelectField
####
from django.contrib.auth.models import User
from django.views.generic import ListView
####
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
# Create your models here.
#User = settings.AUTH_USER_MODEL

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    """
    CHOICES = [
        ('자료실',(
                ('DS','알고리즘'),
                ('AI','인공지능'),
                ('APP','웹앱&모바일앱'),
                ('CG','컴퓨터 그래픽스'),
                ('DB','데이터베이스'),
                ('ETC','기타')
            )
        ),
        ('동아리',(
                ('BB','컴스켓'),
                ('FB','AC잎새'),
                ('HH','YBRO'),
                ('RM','소음')

            )
        ),
        ('소셜',(
                ('JOB','채용공고'),
                ('PJ','프로젝트'),
                ('CC','잡담'),
                ('Q','건의')
        ))
    ]"""
    CHOICES = [(1,'Study'),(2,'Clubs'),(3,'Notice'),(4,'Social')]
    #category = models.CharField(max_length=50) : creates querystring
    category = MultiSelectField(choices=CHOICES,max_choices=1) #makes post.category to be the query
    #image = models.ImageField(blank=True, null=True, upload_to='images/')
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    ####
    likes = models.IntegerField(default=0) #related to Preference model
    dislikes = models.IntegerField(default=0)
    ####

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '[{}]:{}'.format(self.category, self.title)

def path_image_path(instance, filename):
    return f'yblog/{instance.post.pk}/{filename}'

class Image(models.Model):
    post = models.ForeignKey('yblog.Post', default=None, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to= path_image_path,
        #processors = [ResizeToFill(100,50)],
        #format='PNG',
        #options = {'quality':1000},
    )

class Comment(models.Model):
    post = models.ForeignKey('yblog.Post', on_delete=models.CASCADE, related_name = "comments")
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

####
class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) + ':' + str(self.value)

    class Meta:
        unique_together = ["user","post","value"]
####

class PostList(ListView):
    paginate_by = 2
    model = Post

