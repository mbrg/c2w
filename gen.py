import datetime
import os
import random
import string
from openai import OpenAI
import itertools

OPENAI_API_KEY = ""
STRING_LEN = 3

blog_site_title = "Human Who Code"
blog_site_description = "A blog focused on exploring the latest trends, technologies, and gadgets in the tech industry."
prompt_template = """
Given the following blog site title and description, generate a suitable blog post title, relevant tags, and a brief content outline. Make the title as different as possible from the previous titles also provided as input, in terms of content, and vocabulary and style . The blog post should be written in Markdown format and include a YAML prefix. Only output the Markdown content without any additional descriptions. Make sure you close the yml section at the beginning with a --- before you start writing the content.


**Blog Site Title:** {blog_site_title}
**Blog Site Description:** {blog_site_description}
**Previous Post Titles:** {prev_titles}

**Markdown Format:**

---
title: "[Generated Blog Post Title]"
categories:
  - Blog
tags:
  - [Tag 1]
  - [Tag 2]
  - [Additional Tags as needed]
---

# Introduction
[Brief introduction]

## Main Points
### Subheading 1
[Key points under subheading 1]

### Subheading 2
[Key points under subheading 2]

...

# Additional Sections (if needed)
[Content for additional sections]

# Conclusion
[Recap of key points and final thoughts]
"""

def generate_blog_post(blog_site_title, blog_site_description, prev_titles):
    # Fill in the prompt template with the provided blog site title and description
    prompt = prompt_template.format(
        blog_site_title=blog_site_title,
        blog_site_description=blog_site_description,
        prev_titles=prev_titles
    )

    # Call the OpenAI API with the prepared prompt
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that generates blog posts."
        },
        {
            "role": "user",
            "content": prompt
        }
    ])

    # Extract and return the generated blog content
    return response.choices[0].message.content.strip()

def generate_all_strings(STRING_LEN):
    chars = string.ascii_lowercase + string.digits #+ '+/'
    return [''.join(i) for i in itertools.product(chars, repeat=STRING_LEN)]

def generate_random_date():
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=10*365)
    return start + (end - start) * random.random()

all_titles = []
for random_string in generate_all_strings(STRING_LEN):
    random_date = generate_random_date().strftime('%Y-%m-%d')
    filename = f"_posts/{random_date}-{random_string}.md"
    
    all_random_string = [fname[11:-3] for fname in os.listdir("_posts/")]
    if random_string in all_random_string:
        # skip
        continue
    
    # Use OpenAI API to generate TITLE and TAGS
    post = generated_blog_content = generate_blog_post(blog_site_title, blog_site_description, prev_titles=all_titles)
    if "---\n\n# Introduction" not in post:
        post = post.replace("\n# Introduction", "---\n\n# Introduction")
    
    try:
        title = post.split("\n")[1].split(": ")[1]
        all_titles.append(title)
    except IndexError:
        print(f"Skip {random_string} for malformed title.")
        continue

    # Create a new file in _posts/ directory
    with open(filename, 'w') as f:
        f.write(post)
    print(f"File {filename} created. {post.split("\n")[1]}.")