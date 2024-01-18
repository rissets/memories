import pandas as pd
import numpy as np
import ast
import re
from sklearn import metrics
from blog.models import Post, Category
from django.contrib.auth.models import User


df = pd.read_csv('models/output_dataset.csv')

for index, row in df.iterrows():
    Post.objects.create(
        title=row['title'],
        category=Category.objects.get_or_create(name=row['category'])[0],
        excerpt=row['abstract'],
        content=row['abstract'],
        author=User.objects.get(pk=1),
        encodings=row['encodings'],
        status=True,
    )