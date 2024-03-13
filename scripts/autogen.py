from urllib.parse import urlparse
from pathlib import Path

import requests
import hashlib
import shutil
import base64
import json
import os

README = """
  <div align="center">
  
  # 서종찬 Github Page
  
  </div>
  
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FSeo-Faper&count_bg=%23005288&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

---

<div align="center">

## Language & Tools

  <img height="60" width="60" src="https://cdn.simpleicons.org/javascript/#F7DF1E" />
  <img height="60" width="60" src="https://cdn.simpleicons.org/python/#3776AB" />
  <img height="60" width="60" src="https://cdn.simpleicons.org/React/#61DAFB" />
  <br>

<img src="https://img.shields.io/badge/RenPy-FF7F7F?style=for-the-badge&logo=RenPy&logoColor=white">
    <img height="32" width="32" src="https://cdn.simpleicons.org/visualstudiocode/#007ACC" />

<img src="https://img.shields.io/badge/KaliLinux-557C94?style=for-the-badge&logo=KaliLinux&logoColor=white">
  <img height="32" width="32" src="https://cdn.simpleicons.org/vim/#019733" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=React&logoColor=white">
</div>

## Awards

- 2021 군 장병 공개 SW 해커톤 최우수 🎖️ 국방부장관상
- 2022 해군 창업 경진 대회 수상
- 2023 KDFS Challenge 대상 🎖️ 경찰청장상

## Certificates

- 2020 리눅스 마스터 2급
- 2021 네트워크 관리사 2급
- 2021 인터넷 보안 전문가 2급

## Organizations

- Korea Navy CERT (2021. 04. 05 ~2022. 12. 04)
- Best of the Best 12 th Digital Forensics (2023. 07. 01 ~2024. 03. 22)
- Team H4C / D4C

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

        readme_file.write(f'<a href="https://www.github.com/Seo-Faper/{project["id"]}">\n')
        readme_file.write(f'    <img src="images/{project["id"]}.svg" alt="{project["title"]}" align="left" />\n')
        readme_file.write(f'</a>\n\n')
