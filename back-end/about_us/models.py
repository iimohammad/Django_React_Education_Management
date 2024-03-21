from django.db import models
class University(models.Model):
    name = models.CharField(max_length=100, verbose_name='University_name')
    foundation_year = models.PositiveIntegerField(max_length=100 ,verbose_name='Establish_year')
    address = models.CharField(max_length=200, verbose_name='address')
    phone_number = models.CharField(max_length=20, verbose_name='phone')

    def __str__(self):
        return self.name
    
class SocialMediaLinks(models.Model):
    facebook = models.URLField(blank=True, verbose_name='facebook_link')
    twitter = models.URLField(blank=True, verbose_name='twitter_link')
    instagram = models.URLField(blank=True, verbose_name='instagram_link')
    linkedin = models.URLField(blank=True, verbose_name='linkdin_link')
    youtube = models.URLField(blank=True, verbose_name='youtube_link')

    def __str__(self):
        return 'SocialMediaLinks'
class AboutUs(models.Model):
    university = models.OneToOneField(University, on_delete=models.CASCADE, related_name='about_us', verbose_name='دانشگاه')
    email = models.EmailField(max_length=200, verbose_name='Communication email')
    description = models.TextField(blank=True, verbose_name='Description')
    chancellor_name = models.CharField( max_length=200,verbose_name = 'Universty_manger_name')
    chancellor_email = models.EmailField(max_length=200,verbose_name='University_manager_email') 
    total_students = models.PositiveIntegerField(max_length=200,verbose_name='number of student')
    website_url = models.URLField(max_length=200,verbose_name='Website')

    def __str__(self):
        return f'about_us- {self.university.name}'