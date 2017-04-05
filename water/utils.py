from post_office import mail


def send_email_for_test():
    mail.send(
        'chharry@gmail.com',
        'chharry@gmail.com',
        subject='My email',
        message='Hi there!',
        html_message='Hi <strong>there</strong>!',
    )
