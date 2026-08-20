import streamlit as st
import streamlit.components.v1 as components
import os
from PIL import Image

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

st.title("📦 품번 이미지 조회 시스템")
st.markdown("조회할 제품의 품번을 입력해 주세요.")

IMAGE_FOLDER = "images" 
TEMP_FOLDER = "temp_images" # 임시 저장 폴더

# 임시 폴더가 없으면 생성
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

with st.form(key="search_form"):
    product_id = st.text_input("🔍 품번 입력", placeholder="예: a123 또는 A123")
    submit_button = st.form_submit_button("이미지 검색", use_container_width=True)

if submit_button:
    if product_id:
        search_term = product_id.strip().lower()
        found = False
        
        if os.path.exists(IMAGE_FOLDER):
            for filename in os.listdir(IMAGE_FOLDER):
                name, ext = os.path.splitext(filename)
                
                if name.lower() == search_term and ext.lower() in ['.jpg', '.jpeg', '.png']:
                    file_path = os.path.join(IMAGE_FOLDER, filename)
                    
                    # 1. 이미지를 안전하게 오픈하여 임시 폴더에 정식 파일로 저장
                    image = Image.open(file_path)
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    temp_file_name = f"temp_{name}.jpg"
                    temp_file_path = os.path.join(TEMP_FOLDER, temp_file_name)
                    image.save(temp_file_path, "JPEG")
                    
                    st.success(f"✅ 품번 [{name}] 검색 완료")
                    
                    # 2. 진짜 파일 경로를 HTML에 직접 주입 (스트림릿이 차단하지 않음!)
                    # Streamlit은 앱 폴더 내의 파일을 웹 경로로 자동 매핑해 줍니다.
                    img_url = f"app/{temp_file_path}" if os.path.exists(temp_file_path) else temp_file_path
                    # 상대 경로 매핑을 위해 안정적인 경로 설정
                    img_url = f"./{temp_file_path}"
                    
                    components.html(f'''
                    <div style="text-align: center; font-family: sans-serif;">
                        <img id="target-img" src="{img_url}" 
                             style="width: 100%; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <p style="color: gray; font-size: 13px; margin-top: 10px;">
                            👆 사진을 터치하면 <b>확대 팝업 레이어</b>가 열립니다.
                        </p>
                    </div>

                    <script>
                    const imgElement = document.getElementById('target-img');
                    
                    imgElement.onclick = function() {{
                        const parentDoc = window.parent.document;
                        
                        // 기존 레이어 제거
                        let oldLayer = parentDoc.getElementById('html-lightbox');
                        if (oldLayer) oldLayer.remove();
                        
                        // 풀스크린 팝업 레이어 생성
                        const overlay = parentDoc.createElement('div');
                        overlay.id = 'html-lightbox';
                        overlay.style.position = 'fixed';
                        overlay.style.top = '0';
                        overlay.style.left = '0';
                        overlay.style.width = '100vw';
                        overlay.style.height = '100vh';
                        overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.95)';
                        overlay.style.zIndex = '9999999';
                        overlay.style.display = 'flex';
                        overlay.style.justifyContent = 'center';
                        overlay.style.alignItems = 'center';
                        overlay.style.overflow = 'auto';

                        // 레이어 안의 이미지 (두 손가락 확대/축소 가능)
                        const bigImg = parentDoc.createElement('img');
                        bigImg.src = '{img_url}';
                        bigImg.style.maxWidth = '100%';
                        bigImg.style.maxHeight = '100%';
                        bigImg.style.objectFit = 'contain';
                        bigImg.style.touchAction = 'pinch-zoom';

                        // 배경이나 사진을 터치하면 닫힘
                        overlay.onclick = function() {{
                            overlay.remove();
                        }};

                        overlay.appendChild(bigImg);
                        parentDoc.body.appendChild(overlay);
                    }};
                    </script>
                    ''', height=400)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
