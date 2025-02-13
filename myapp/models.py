from django.db import models

class Streak(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.count}"

class userDetails(models.Model):
    user=models.CharField(max_length=50)
    password=models.CharField(max_length=50)