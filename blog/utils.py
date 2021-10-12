import math
import random
import re
import string

from django.utils import html
from django.utils.html import strip_tags


def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0) #assuming 200wpm reading
    return int(read_time_min)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def user_directory_path(instance, filename):
    return "posts/{0}/{1}".format(instance.pub_date.strftime('%m-%d-%Y'), filename)

