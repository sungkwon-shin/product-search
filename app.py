<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>품번 조회 뷰어</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; }
        .search-box { padding: 10px; width: 80%; font-size: 16px; margin-bottom: 20px; }
        .img-container { display: flex; flex-direction: column; align-items: center; }
        img { width: 100%; max-width: 500px; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>

    <h2>📦 품번 이미지 조회</h2>
    <input type="text" id="searchInput" class="search-box" placeholder="품번 입력 (예: a123)">
    <div id="result"></div>

    <script>
        // 이미지 검색 로직
        document.getElementById('searchInput').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                const term = this.value.trim().toLowerCase();
                // 여기에 이미지 폴더의 경로를 매칭 (이미지 파일명이 예: a123.jpg 라고 가정)
                const imgPath = 'images/' + term + '.jpg'; 
                
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `
                    <p>✅ 품번 [${term}] 검색 완료</p>
                    <img src="${imgPath}" onclick="openViewer(this.src)" onerror="this.onerror=null;this.src='error.png';alert('이미지를 찾을 수 없습니다.')">
                `;
            }
        });

        // 클릭하면 전체화면으로 열리고, 다시 누르면 닫히는 가장 순수한 뷰어 로직
        function openViewer(src) {
            const overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0'; overlay.style.left = '0';
            overlay.style.width = '100vw'; overlay.style.height = '100vh';
            overlay.style.backgroundColor = 'rgba(0,0,0,0.95)';
            overlay.style.zIndex = '9999';
            overlay.style.display = 'flex';
            overlay.style.justifyContent = 'center';
            overlay.style.alignItems = 'center';
            overlay.onclick = () => overlay.remove(); // 배경 아무 데나 누르면 닫힘

            const img = document.createElement('img');
            img.src = src;
            img.style.maxWidth = '100%';
            img.style.maxHeight = '100%';
            
            overlay.appendChild(img);
            document.body.appendChild(overlay);
        }
    </script>
</body>
</html>
