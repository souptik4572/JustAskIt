from django.db import models
# Create your models here.


class EndUser(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=320, unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=256)
    description = models.CharField(max_length=500)
    profile_image = models.CharField(max_length=256, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Location(models.Model):
    user = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=320)
    start_year = models.DateField()
    end_year = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.location}"


class Education(models.Model):
    user = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    school = models.CharField(max_length=256)
    degree_type = models.CharField(max_length=60)
    graduation_year = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.school}"


class Employment(models.Model):
    user = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=256)
    start_year = models.DateField()
    end_year = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.position} - {self.company}"


class Follow(models.Model):
    follower = models.ForeignKey(
        EndUser, on_delete=models.CASCADE, related_name='follower_id')
    followee = models.ForeignKey(
        EndUser, on_delete=models.CASCADE, related_name='followee_name')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower.name} follows {self.followee.name}"

class Token(models.Model):
    user = models.ForeignKey(
        EndUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
