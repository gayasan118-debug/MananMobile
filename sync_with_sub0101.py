
import os
import re

# 대상 파일 리스트
files_map = {
    '.': ['index.htm'],
    'contents': [f for f in os.listdir('contents') if f.endswith('.html')],
    'bbs': [f for f in os.listdir('bbs') if f.endswith('.html')]
}

# sticky_bottom_bar 영역 찾기
pattern = re.compile(r'<div class="sticky_bottom_bar">.*?</div>', re.DOTALL)

# sub01_01.php.html 에서 확인된 '정상' 코드 (이모지 포함, 한글 텍스트)
base_code = """<div class="sticky_bottom_bar">
    <a href="tel:1688-0458" class="call_btn">
        <span class="icon">📞</span>
        <span class="txt">전화상담</span>
    </a>
    <a href="LINK_PLACEHOLDER" class="reg_btn">
        <span class="icon">📝</span>
        <span class="txt">관심고객등록</span>
    </a>
</div>"""

def get_code(dir_path):
    link = ""
    if dir_path == '.':
        link = "bbs/write.php.html?bo_table=customer"
    elif dir_path == 'contents':
        link = "../bbs/write.php.html?bo_table=customer"
    elif dir_path == 'bbs':
        link = "write.php.html?bo_table=customer"
    
    return base_code.replace("LINK_PLACEHOLDER", link)

for dir_path, filenames in files_map.items():
    for filename in filenames:
        filepath = os.path.join(dir_path, filename)
        
        # sub01_01.php.html은 기준 파일이므로 스킵하여 원본 보존
        if filename == 'sub01_01.php.html':
            print(f"Skipping source file: {filepath}")
            continue

        try:
            content = ""
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='cp949') as f:
                    content = f.read()
            
            # 교체
            new_code = get_code(dir_path)
            new_content, count = pattern.subn(new_code, content)
            
            if count > 0:
                # UTF-8로 저장하여 한글/이모지 보존
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Synced with sub01_01: {filepath}")
            else:
                print(f"No match found: {filepath}")

        except Exception as e:
            print(f"Error processing {filepath}: {e}")
