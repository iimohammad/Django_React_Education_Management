from accounts.models import User


class Admin(User):
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
