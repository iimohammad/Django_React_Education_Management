from django.db import models

class ContactInfo(models.Model):
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.address

class University(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    contactInfo = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    website_url = models.URLField(max_length=200)
    social_media_links = models.JSONField()

    def __str__(self):
        return self.name

class Comment(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=100 , blank=True, null=True) 
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
