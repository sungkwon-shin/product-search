import streamlit as st
import streamlit.components.v1 as components
import os
from PIL import Image

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

# [핵심] 스트림릿이 강제로 막아둔 '모바일 줌(Zoom)' 기능을 강제로 풀어버리는 스크립트
components.html(
    """
    <script>
    const parent = window.parent.document;
    let meta = parent.querySelector('meta[name="viewport"]');
    if (meta) {
        meta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
    }
    </script>
    """,
    height=0, width=0
)

st.title("📦 품번 이미지 조회 시스템")
st.markdown("조회할 제품의 품번을 입력해 주세요.")

IMAGE_FOLDER = "images" 

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
                    image = Image.open(file_path)
                    
                    st.success(f"✅ 품번 [{name}] 검색 완료")
                    
                    # 팝업이나 버튼 없이 그냥 화면에 출력합니다.
                    st.image(image, caption="👆 두 손가락으로 화면을 쫙 벌려 확대해 보세요.", use_container_width=True)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
