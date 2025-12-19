## EmailJS 설정 안내

EmailJS를 사용하여 이메일 전송 기능을 활성화하려면 다음 단계를 따르세요:

### 1. EmailJS 계정 생성 및 로그인

아직 EmailJS 계정이 없다면 [EmailJS 웹사이트](https://www.emailjs.com/)에서 계정을 생성하고 로그인하세요.

### 2. Service ID, Template ID, Public Key 확인

로그인 후, EmailJS 대시보드에서 다음 정보를 찾거나 생성해야 합니다.

*   **Service ID (서비스 ID):**
    *   `Email Services` 메뉴에서 이메일 서비스를 추가합니다 (예: Gmail, Outlook). 서비스 추가 시 생성되는 ID입니다.
    *   새 스크립트 코드의 `'YOUR_SERVICE_ID'` 부분을 이 값으로 변경해야 합니다.

*   **Template ID (템플릿 ID):**
    *   `Email Templates` 메뉴에서 새 이메일 템플릿을 생성합니다. 템플릿 생성 시 자동으로 ID가 부여됩니다.
    *   새 스크립트 코드의 `'YOUR_TEMPLATE_ID'` 부분을 이 값으로 변경해야 합니다.
    *   **템플릿 내용 설정:** 템플릿 본문에는 폼에서 전송되는 데이터를 받을 수 있도록 변수를 설정해야 합니다. 예를 들어, HTML 템플릿에서 다음과 같이 설정할 수 있습니다:
        ```html
        <p>이름: {{wr_name}}</p>
        <p>휴대전화: {{full_phone}}</p>
        <p>문의 내용: {{wr_5}}</p>
        <p>선호타입: {{wr_type}}</p>
        <p>개인정보 수집 및 이용 동의: {{agree1}}</p>
        <p>마케팅 활용 동의: {{wr_10}}</p>
        ```
    *   **수신자 이메일 설정:** 템플릿 설정의 `Recipient` 섹션에서 `To Email` 필드를 `mp1500@naver.com`으로 설정하세요.

*   **Public Key (공개 키 - User ID):**
    *   `Account` -> `API Keys` 메뉴에서 `Public Key` (또는 `User ID`)를 찾을 수 있습니다.
    *   새 스크립트 코드의 `emailjs.init("YOUR_PUBLIC_KEY");` 부분을 이 값으로 변경해야 합니다.

### 3. `bbs/write.php.html` 파일 업데이트

이제 `bbs/write.php.html` 파일에 제가 수정한 스크립트가 적용되어 있습니다. 이 스크립트 내의 플레이스홀더를 위에서 확인한 실제 값으로 변경해야 합니다.

파일을 열고 아래 부분을 찾아서 해당 값을 교체하세요:

```javascript
<script type="text/javascript">
    function sendEmail(event) {
        event.preventDefault(); // 폼의 기본 제출 동작을 막습니다.

        var form = document.getElementById('fwrite');

        // 기존의 폼 유효성 검사 함수를 호출합니다.
        if (!fwrite_submit(form)) {
            return; // 유효성 검사 실패 시 함수를 중단합니다.
        }

        // EmailJS 초기화 (YOUR_PUBLIC_KEY를 실제 Public Key로 변경하세요)
        emailjs.init("YOUR_PUBLIC_KEY"); // <-- 이 부분을 변경하세요

        // 템플릿에 전달할 파라미터를 준비합니다.
        var templateParams = {
            wr_name: form.wr_name.value,
            full_phone: form.hp1.value + '-' + form.hp2.value + '-' + form.hp3.value,
            wr_5: form.wr_5.value,
            wr_type: form.querySelector('input[name="wr_type"]:checked') ? form.querySelector('input[name="wr_type"]:checked').value : '선택 안 함',
            agree1: form.agree1[0].checked ? '동의' : '동의하지 않음',
            wr_10: form.querySelector('input[name="wr_10"]:checked') ? form.querySelector('input[name="wr_10"]:checked').value : '선택 안 함'
        };

        // EmailJS를 통해 이메일을 보냅니다.
        // 'YOUR_SERVICE_ID'와 'YOUR_TEMPLATE_ID'를 실제 값으로 변경하세요.
        emailjs.send('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', templateParams) // <-- 이 두 부분을 변경하세요
            .then(function(response) {
               console.log('SUCCESS!', response.status, response.text);
               alert('관심고객 등록이 성공적으로 완료되었습니다.');
               window.location.reload(); // 성공 시 페이지를 새로고침합니다.
            }, function(error) {
               console.log('FAILED...', error);
               alert('관심고객 등록에 실패했습니다. 다시 시도해주세요.');
            });
    }
</script>
```

이 단계를 완료하면 폼 제출 시 EmailJS를 통해 `mp1500@naver.com`으로 이메일이 전송될 것입니다.