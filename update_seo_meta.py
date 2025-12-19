
import os
import re

# 대상 디렉토리
target_dirs = ['.', 'contents', 'bbs']

# 적용할 메타 태그 내용
meta_desc = '월판선 만안역(예정) 초역세권 프리미엄, 안양 만안구 신축 아파트 분양 정보. KTX광명역세권 생활권 공유.'
og_title = '만안역 중앙하이츠 포레 - 공식 분양안내'
og_desc = meta_desc
og_url = 'https://xn--om2b95a99s7bt4be5et2dc4ov7m6nd.shop'

def update_meta_tags(filepath):
    try:
        content = ""
        encoding = 'utf-8'
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            encoding = 'cp949'
            with open(filepath, 'r', encoding='cp949') as f:
                content = f.read()
        
        original_content = content
        
        # 1. Description 태그 (따옴표 위치 수정됨)
        new_desc_tag = f'<meta name="description" content="{meta_desc}">'
        # 기존 태그 찾기 (대소문자 무시)
        desc_regex = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'][^"\"]*["\"]\s*/*>', re.IGNORECASE)
        
        if desc_regex.search(content):
            content = desc_regex.sub(new_desc_tag, content)
        else:
            if '</title>' in content:
                content = content.replace('</title>', f'</title>\n{new_desc_tag}')
            elif '<head>' in content:
                content = content.replace('<head>', f'<head>\n{new_desc_tag}')

        # 2. Open Graph 태그들
        og_tags = {
            'og:title': og_title,
            'og:description': og_desc,
            'og:type': 'website',
            'og:url': og_url
        }

        for prop, val in og_tags.items():
            new_og_tag = f'<meta property="{prop}" content="{val}">'
            og_regex = re.compile(rf'<meta\s+property=["\']{prop}["\']\s+content=["\'][^"\"]*["\"]\s*/*>', re.IGNORECASE)
            
            if og_regex.search(content):
                content = og_regex.sub(new_og_tag, content)
            else:
                # description 태그 뒤에 차례로 붙임
                content = content.replace(new_desc_tag, f'{new_desc_tag}\n{new_og_tag}')

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated meta tags: {filepath}")
        else:
            print(f"Already up-to-date: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# 실행
for dir_path in target_dirs:
    if dir_path == '.':
        for filename in os.listdir('.'):
            if filename.endswith('.htm') or filename.endswith('.html'):
                update_meta_tags(filename)
    elif os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            if filename.endswith('.htm') or filename.endswith('.html'):
                update_meta_tags(os.path.join(dir_path, filename))
