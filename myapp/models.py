from django.db import models

class Streak(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.count}"
