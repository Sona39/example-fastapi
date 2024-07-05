import random
import string

def generate_random_email(domain="example.com", length=10):
    letters = string.ascii_letters + string.digits
    username = ''.join(random.choice(letters) for _ in range(length))
    return f"{username}@{domain}"

def generate_random_post_title(length=10):
    letters = string.ascii_letters + string.digits
    title = ''.join(random.choice(letters) for _ in range(length))
    return f"title  {title}"

def generate_random_post_content(length=30):
    letters = string.ascii_letters + string.digits
    content = ''.join(random.choice(letters) for _ in range(length))
    return f"content {content}"