from urllib.parse import urlparse
from pathlib import Path

import requests
import hashlib
import shutil
import base64
import json
import os

README = """
Hello world! 👋  
My name is David and I'm a Software Engineer.  
Over here you'll find some side projects I work on from time to time.

### Featured Projects

"""

base_path = Path(__file__).resolve().parent

def get_url_image_extension(url):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext

def write_image_to_file(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)    


def image_url_to_base64(image_url):
    try:
        response = requests.get(image_url)
        
        if response.status_code == 200:
            image_data = response.content
            
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            return base64_image
        else:
            raise Exception(f"Failed to fetch image. Status code: {response.status_code}")
    except Exception:
        raise


with open(base_path / "template.svg",  encoding='UTF8') as template_file,  \
     open(base_path / "database.json",  encoding='UTF8') as database_file, \
     open(base_path / ".." / "README.md", "w", encoding="UTF8") as readme_file:
    
    readme_file.write(README)

    template = template_file.read()
    projects = json.loads(database_file.read())["projects"]

    for project in projects:
        hashed_image_name = f'{hashlib.sha1(project["image"].encode()).hexdigest()}{get_url_image_extension(project["image"])}'
        hashed_image_path = base_path / "cache" / hashed_image_name

        if not hashed_image_path.exists():
            write_image_to_file(project["image"], hashed_image_path)

        with open(hashed_image_path, "rb") as image_file:
            image_b64 = base64.encodebytes(image_file.read()).decode('ascii')

        with open(base_path / ".." / "images" / f"{project['id']}.svg", "w") as out:
            contents = template.replace("##IMG_SRC##", "data:image/png;base64," + image_b64.rstrip())
            contents = contents.replace("##TITLE##", project["title"])
            contents = contents.replace("##DESCRIPTION##", project["description"])
            contents = contents.replace("##ALIGN_IMAGE##", project["align_image"])
            out.write(contents)

        readme_file.write(f'<a href="https://www.github.com/Dvd848/{project["id"]}">\n')
        readme_file.write(f'    <img src="images/{project["id"]}.svg" alt="{project["title"]}" align="left" />\n')
        readme_file.write(f'</a>\n\n')
