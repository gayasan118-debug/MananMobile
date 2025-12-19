
import os
import re

# 변경 대상 파일들이 있는 디렉토리
target_dirs = ['.', 'contents', 'bbs']
extensions = ['.html', '.htm']

# 새로운 네이버 소유확인 메타 태그
new_meta = '<meta name="naver-site-verification" content="982eadd8178dd5a050e7048d5517ade5e7eeb3d9">'

# 기존 네이버 메타 태그를 찾는 정규식 (verification 뒤의 내용 상관없이 찾음)
meta_regex = re.compile(r'<meta\s+name=["\']naver-site-verification["\']\s+content=["\'][^"\']+["\']\s*/>', re.IGNORECASE)

def update_naver_verification(filepath):
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
        
        # 메타 태그가 있으면 교체
        if meta_regex.search(content):
            new_content = meta_regex.sub(new_meta, content)
            
            # 변경 사항이 있으면 저장
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated: {filepath}")
            else:
                print(f"Already up-to-date: {filepath}")
        else:
            # 없으면 head 태그 바로 뒤에 추가 (혹은 title 위에 추가)
            if '<head>' in content:
                new_content = content.replace('<head>', f'<head>\n{new_meta}')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Added new tag: {filepath}")
            else:
                print(f"No head tag found: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# 실행
for dir_path in target_dirs:
    if dir_path == '.':
        for filename in os.listdir('.'):
            if any(filename.endswith(ext) for ext in extensions):
                update_naver_verification(filename)
    elif os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            if any(filename.endswith(ext) for ext in extensions):
                update_naver_verification(os.path.join(dir_path, filename))
