from django.core.mail import EmailMultiAlternatives


def send_email_for_test(articles):
    subject, from_email, to = 'hello', 'chharry@gmail.com', 'chharry@gmail.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'

    for article in articles:
        html_content += "<p>%s</p<br>" % article['title']

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
