import os

# 대상 디렉토리
target_dirs = ['contents', 'bbs']

# 찾을 문자열 (정확히 일치해야 함)
old_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
# 바꿀 문자열
new_viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=3.0, user-scalable=yes">'

def update_viewport(filepath):
    try:
        content = ""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='cp949') as f:
                content = f.read()
        
        if old_viewport in content:
            new_content = content.replace(old_viewport, new_viewport)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated viewport: {filepath}")
        else:
            print(f"Pattern not found (or already updated): {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# 실행
for dir_path in target_dirs:
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            if filename.endswith('.html'):
                update_viewport(os.path.join(dir_path, filename))