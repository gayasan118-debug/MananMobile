
import os

# 변경 대상 파일들이 있는 디렉토리
target_dirs = ['.', 'contents', 'bbs']
# 변경할 파일 확장자
extensions = ['.xml', '.txt', '.html', '.htm', '.js']

# 교체할 도메인 목록 (기존 도메인들)
old_domains = [
    'https://xn--hj2bu5b94r7bt4be5et2dc4ov7m6nd.kr', # .kr
    'https://xn--om2b95a99s7bt4be5et2dc4ov7m6nd.com', # .com
    'http://xn--hj2bu5b94r7bt4be5et2dc4ov7m6nd.kr',
    'http://xn--om2b95a99s7bt4be5et2dc4ov7m6nd.com'
]

# 새로운 도메인
new_domain = 'https://xn--om2b95a99s7bt4be5et2dc4ov7m6nd.shop'

def update_domain(filepath):
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
        
        # 모든 구버전 도메인을 새 도메인으로 교체
        for old in old_domains:
            content = content.replace(old, new_domain)
            
        # 변경 사항이 있으면 저장
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# 디렉토리 순회하며 실행
for dir_path in target_dirs:
    if dir_path == '.':
        # 루트 디렉토리 파일 처리
        for filename in os.listdir('.'):
            if os.path.isfile(filename) and any(filename.endswith(ext) for ext in extensions):
                update_domain(filename)
    elif os.path.exists(dir_path):
        # 서브 디렉토리 파일 처리
        for filename in os.listdir(dir_path):
            if any(filename.endswith(ext) for ext in extensions):
                update_domain(os.path.join(dir_path, filename))
