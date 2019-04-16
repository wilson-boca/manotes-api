from app import exceptions
from app.async_tasks import tasks
from app.house import services
from app.security import security_services


class Clerk(object):

    @classmethod
    def create_user_account(cls, user):
        user['password'] = security_services.HashService.hash(user['password'])
        user['token'] = security_services.TokenService.generate()
        if not security_services.ValidationService.is_email(user['email']):
            raise exceptions.InvalidEmail('Could not create user account because the email: {} is invalid'.format(user['email']))
        created_user = services.UserService.create_new(user)
        name = created_user.username
        from_address = "wilson.boca@gmail.com"
        to_address = created_user.email
        subject = "Test"
        tasks.start_send_email(name, from_address, to_address, subject)
        return created_user
