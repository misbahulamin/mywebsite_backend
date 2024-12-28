from django.db import models

class MyProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    key_features = models.TextField()
    technology_stack = models.TextField()
    my_role = models.TextField()
    thumbnail = models.ImageField(upload_to='portfolio/thumbnail/', blank=True, null=True)
    code_link = models.URLField(blank=True, null=True)
    live = models.URLField(blank=True, null=True)
    challenges_and_learning = models.TextField()

    def __str__(self):
        return self.title