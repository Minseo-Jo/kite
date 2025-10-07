"""
Kite 프론트엔드 (Streamlit)
"""
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# 페이지 설정
st.set_page_config(
    page_title="Kite - 업무 맥락 파악 도우미",
    page_icon="🪁",
    layout="wide"
)

# 타이틀
st.title("🪁 Kite: AI 기반 업무 맥락 파악 도우미")
st.markdown("갑작스러운 업무 요청도 30초 안에 이해하세요!")

st.divider()

# 사용자 입력
col1, col2 = st.columns([4, 1])
with col1:
    user_query = st.text_input(
        "업무 관련 질문을 입력하세요",
        placeholder="예: Redis Stream 테이블 설계가 뭐야?",
        key="query_input"
    )
with col2:
    st.write("")  # 간격 조정
    analyze_button = st.button("🔍 분석 시작", type="primary", use_container_width=True)

# 예시 질문 버튼
st.markdown("**💡 예시 질문:**")
col_ex1, col_ex2, col_ex3 = st.columns(3)
with col_ex1:
    if st.button("Redis Stream 테이블 설계란?"):
        user_query = "Redis Stream 테이블 설계란?"
        analyze_button = True
with col_ex2:
    if st.button("CHUB 프로젝트가 뭐야?"):
        user_query = "CHUB 프로젝트가 뭐야?"
        analyze_button = True
with col_ex3:
    if st.button("이 업무의 마감일은?"):
        user_query = "이 업무의 마감일은?"
        analyze_button = True

st.divider()

# 분석 실행
if analyze_button and user_query:
    with st.spinner("🔎 관련 문서를 찾고 AI가 분석하고 있습니다..."):
        try:
            # FastAPI 호출
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                json={"query": user_query},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 업무 맥락 요약
                st.subheader("📖 업무 맥락 요약")
                st.markdown(result["summary"])
                
                st.divider()
                
                # 관련 문서
                st.subheader(f"🔍 관련 문서 ({len(result['documents'])}개 발견)")
                for doc in result["documents"]:
                    with st.expander(f"**[{doc['source']}]** {doc['title']} | {doc['date']}"):
                        st.write(doc["content"])
                        if "sender" in doc:
                            st.caption(f"작성자: {doc.get('sender', doc.get('author', doc.get('assignee', '')))}")
                st.divider()
                
                # 액션 아이템
                st.subheader("✅ 해야 할 일 (Action Items)")
                for i, item in enumerate(result["action_items"], 1):
                    st.checkbox(f"{i}. {item}", key=f"action_{i}")
                
            else:
                st.error(f"❌ 서버 오류: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ 백엔드 서버에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인하세요.")
        except Exception as e:
            st.error(f"❌ 오류 발생: {str(e)}")

# 사이드바
with st.sidebar:
    st.header("ℹ️ 사용 방법")
    st.markdown("""
    1. 위 입력창에 업무 관련 질문 입력
    2. **분석 시작** 버튼 클릭
    3. AI가 관련 문서를 찾아 맥락 요약
    4. 해야 할 일 목록 확인
    """)
    
    st.divider()
    
    st.header("🎯 프로토타입 기능")
    st.markdown("""
    - ✅ AI 기반 업무 맥락 요약
    - ✅ 다중 채널 문서 통합 표시
    - ✅ 액션 아이템 자동 추출
    """)