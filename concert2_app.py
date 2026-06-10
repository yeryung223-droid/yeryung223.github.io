"""
Concert Survey, Dashboard & Content Platform — Light Theme
==========================================================
실행: streamlit run concert_survey_app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── 1. 페이지 및 라이트 테마 설정 ──────────────────────────────
st.set_page_config(
    page_title="Concert Hub & Survey",
    page_icon="🎵",
    layout="wide",
)

# 화이트 & 인디고 & 민트 기반의 트렌디한 라이트 테마 CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { 
    font-family: 'Pretendard', sans-serif; 
    background-color: #f8fafc !important; 
    color: #1e293b; 
}
.stApp { background-color: #f8fafc !important; }

/* 섹션 스타일 */
.section-lbl {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #6366f1; margin-bottom: 0.4rem;
}
.section-ttl {
    font-size: 2rem; font-weight: 700; color: #0f172a; line-height: 1.2; margin-bottom: 1.5rem;
}
.section-ttl em { color: #10b981; font-style: normal; }

/* 커스텀 카드 디자인 */
.custom-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 1.6rem; margin-bottom: 1.2rem; height: 100%;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
}

/* 아티스트 추천 뱃지 카드 */
.artist-card {
    background: linear-gradient(135deg, #eff6ff, #ffffff);
    border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;
}

/* 설문 폼 헤더 */
.survey-header {
    background: linear-gradient(135deg, #f1f5f9, #ffffff);
    border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;
}

/* Metric 스타일 */
[data-testid="metric-container"] {
    background: #ffffff !important; border: 1px solid #e2e8f0 !important; 
    border-radius: 12px !important; padding: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
</style>
""", unsafe_allow_html=True)


# ── 2. 데이터베이스 초기화 (확장된 7개 문항 반영) ─────────────────
if "survey_db" not in st.session_state:
    st.session_state.survey_db = pd.DataFrame([
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 160, "sat": 5, "genre": "K-POP / 아이돌", "with_who": "친구 / 동료"},
        {"age": "20대", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 95, "sat": 4, "genre": "밴드 / 록 / 인디", "with_who": "연인"},
        {"age": "10대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 45, "sat": 3, "genre": "K-POP / 아이돌", "with_who": "혼자(혼콘)"},
        {"age": "30대 이상", "freq": "거의 안 간다", "seat": "중간 좌석", "spend": 80, "sat": 3, "genre": "힙합 / R&B", "with_who": "가족"},
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 210, "sat": 5, "genre": "EDM / 페스티벌", "with_who": "친구 / 동료"},
    ])


# ── 3. 상단 GNB 내비게이션 바 ──────────────────────────────────
st.markdown("""
<div style="background:#ffffff; border-bottom:1px solid #e2e8f0; padding:1rem 2rem; display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem;">
  <span style="font-family:'IBM Plex Mono',monospace; font-size:1.2rem; font-weight:700; color:#6366f1;">
    CONCERT<span style="color:#10b981;">.</span>PLAYGROUND
  </span>
  <span style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#64748b; letter-spacing:0.1em;">
    SURVEY & AUDIENCE MAGAZINE · 2026
  </span>
</div>
""", unsafe_allow_html=True)


# ── Tab 구조로 볼거리 분리 (1. 참여&통계 / 2. 아티스트 추천&볼거리) ──
tab1, tab2 = st.tabs(["📊 설문참여 및 실시간 데이터", "✨ 취향 추천 및 트렌드 매거진"])

with tab1:
    # ── 4. 입력 섹션 (좌측 폼 / 우측 로그) ────────────────────────
    col_input, col_recent = st.columns([1.2, 1], gap="large")

    with col_input:
        st.markdown('<p class="section-lbl">01 — EXPANDED SURVEY</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-ttl">관객 <em>트렌드</em> 설문조사</p>', unsafe_allow_html=True)
        
        with st.form(key="expanded_survey_form", clear_on_submit=True):
            st.markdown("""
            <div class="survey-header">
                <span style="color:#6366f1; font-weight:700; font-size:0.9rem;">📢 질문이 추가되었습니다!</span>
                <p style="font-size:0.85rem; color:#475569; margin-top:4px;">당신의 콘서트 라이프스타일을 더 자세히 들려주세요.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 7개 확장 문항
            q1 = st.segmented_control("Q1. 연령대", ["10대", "20대", "30대 이상"], default="20대")
            q2 = st.selectbox("Q2. 평소 공연 관람 빈도", ["자주 간다", "가끔 간다", "거의 안 간다"])
            q3 = st.radio("Q3. 주로 예매하는 티켓 구역", ["VIP 좌석", "중간 좌석", "저가 좌석"], horizontal=True)
            q4 = st.slider("Q4. 콘서트 1회당 평균 지출 티켓 값 ($)", 0, 300, 120, step=5)
            q5 = st.select_slider("Q5. 최근 직관한 공연의 전반적인 만족도", options=[1, 2, 3, 4, 5], value=4)
            
            st.divider()
            # 신규 추가된 깊이 있는 질문들
            q6 = st.selectbox("Q6. 가장 선호하는 음악 및 콘서트 장르는?", ["K-POP / 아이돌", "밴드 / 록 / 인디", "힙합 / R&B", "EDM / 페스티벌", "클래식 / 뮤지컬"])
            q7 = st.radio("Q7. 콘서트는 주로 누구와 함께 가시나요?", ["혼자(혼콘)", "친구 / 동료", "연인", "가족"], horizontal=True)
            
            st.write("")
            submit = st.form_submit_button("🚀 설문 데이터 전송하기")
            
            if submit:
                new_row = pd.DataFrame([{"age": q1, "freq": q2, "seat": q3, "spend": q4, "sat": q5, "genre": q6, "with_who": q7}])
                st.session_state.survey_db = pd.concat([st.session_state.survey_db, new_row], ignore_index=True)
                st.toast("통계 대시보드에 즉시 실시간 반영되었습니다!", icon="🔥")
                st.rerun()

    with col_recent:
        st.markdown('<p class="section-lbl">02 — REAL-TIME LOG</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-ttl">실시간 <em>관객</em> 응답 피드</p>', unsafe_allow_html=True)
        
        data_log = st.session_state.survey_db.iloc[::-1].copy()
        data_log.columns = ["연령대", "빈도", "좌석", "지출($)", "만족도", "선호장르", "동행인"]
        
        st.dataframe(data_log, use_container_width=True, height=520)

    # ── 5. 실시간 대시보드 시각화 ──────────────────────────────
    st.divider()
    st.markdown('<p class="section-lbl">03 — VISUALIZATION</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">통계 <em>차트</em> 분석</p>', unsafe_allow_html=True)

    df = st.session_state.survey_db
    
    # 상단 메트릭 요약
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("총 응답 데이터", f"{len(df)}건")
    m2.metric("관객 평균 지출액", f"${df['spend'].mean():.1f}")
    m3.metric("가장 핫한 장르", f"{df['genre'].mode()[0]}")
    m4.metric("주요 동행인 유형", f"{df['with_who'].mode()[0]}")
    
    st.write("")
    
    CHART_THEME = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#1e293b"))
    GRID_STYLE = dict(gridcolor="#e2e8f0", zeroline=False)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='custom-card'><strong>🎵 관객 선호 음악 장르 비율</strong>", unsafe_allow_html=True)
        genre_val = df["genre"].value_counts()
        fig1 = go.Figure(go.Pie(labels=genre_val.index, values=genre_val.values, hole=0.5, marker=dict(colors=["#6366f1", "#10b981", "#f5a623", "#ec4899", "#8b5cf6"])))
        fig1.update_layout(**CHART_THEME, height=260)
        st.plotly_chart(fig1, use_container_width=True, key="genre_chart")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='custom-card'><strong>👥 누구와 함께 관람하나요? (동행인 분포)</strong>", unsafe_allow_html=True)
        with_val = df["with_who"].value_counts()
        fig2 = go.Figure(go.Bar(x=with_val.index, y=with_val.values, marker=dict(color="#10b981", cornerradius=6)))
        fig2.update_layout(**CHART_THEME, height=260)
        fig2.update_yaxes(**GRID_STYLE)
        st.plotly_chart(fig2, use_container_width=True, key="with_chart")
        st.markdown("</div>", unsafe_allow_html=True)


with tab2:
    # ── 6. 아티스트 추천 및 볼거리 매거진 영역 ───────────────────────
    st.markdown('<p class="section-lbl">04 — INTERACTIVE DISCOVERY</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">내 취향 매칭 <em>아티스트 추천</em></p>', unsafe_allow_html=True)
    
    # 인터랙티브 필터링 시스템 구현
    st.write("아래에서 본인이 좋아하는 장르와 예산을 고르면, 맞춤형 아티스트와 추천 공연을 실시간 매칭해 드립니다.")
    
    user_genre = st.selectbox("선호 장르 선택", ["K-POP / 아이돌", "밴드 / 록 / 인디", "힙합 / R&B", "EDM / 페스티벌", "클래식 / 뮤지컬"], key="recommend_genre")
    user_budget = st.slider("내 티켓 예산 한도 ($)", 30, 300, 150, key="recommend_budget")
    
    # 가상 추천 데이터 매핑 아키텍처
    recommendations = {
        "K-POP / 아이돌": [
            {"name": "NewJeans (뉴진스)", "cost": 140, "desc": "트렌디한 이지리스닝의 정수. 완벽한 연출과 압도적인 관객 떼창을 선사하는 팝 콘서트.", "tag": "추천 좌석: 중간~VIP"},
            {"name": "세븐틴 (SEVENTEEN)", "cost": 160, "desc": "화려한 군무와 무대 장악력, 지칠 줄 모르는 앙코르 무대로 유명한 에너지 충전형 공연.", "tag": "예산 초과 주의"}
        ],
        "밴드 / 록 / 인디": [
            {"name": "데이식스 (DAY6)", "cost": 110, "desc": "모든 관객이 올스탠딩으로 한 목소리가 되는 감성 충만 떼창 맛집 밴드 콘서트.", "tag": "가성비 탑"},
            {"name": "실리카겔 (Silica Gel)", "cost": 85, "desc": "폭발적인 사이키델릭 사운드와 화려한 미디어 아트 빔 연출이 돋보이는 가장 핫한 인디 록 무대.", "tag": "매니아 강추"}
        ],
        "힙합 / R&B": [
            {"name": "박재범 (Jay Park)", "cost": 120, "desc": "그루브한 R&B 감성부터 파워풀한 힙합 레이블 크루들과의 합동 무대까지 완성도 높은 파티형 콘서트.", "tag": "핫 페스티벌 무드"},
            {"name": "딘 (DEAN)", "cost": 90, "desc": "독보적인 음색과 트렌디한 무대 셋팅으로 차분하면서도 칠(Chill)한 감성을 채워주는 라이브 무대.", "tag": "조용한 전율"}
        ],
        "EDM / 페스티벌": [
            {"name": "울트라 코리아 2026 (UMF)", "cost": 180, "desc": "글로벌 최정상 DJ 라인업과 함께 밤새 야외에서 뛰어놀 수 있는 일렉트로닉 댄스 뮤직의 심장.", "tag": "체력 필수"},
            {"name": "페스티벌 붐업 (Boom Up)", "cost": 70, "desc": "국내 DJ들과 힙한 아티스트들이 대거 참여하는 가성비 최고조의 여름 밤 풀파티 페스티벌.", "tag": "가성비 여름축제"}
        ],
        "클래식 / 뮤지컬": [
            {"name": "조성진 피아노 리사이틀", "cost": 150, "desc": "세계가 인정하는 거장의 섬세하고도 강렬한 터치, 완벽한 음향 홀에서 느끼는 정통 클래식의 전율.", "tag": "품격 있는 선택"},
            {"name": "뮤지컬 <레미제라블>", "cost": 130, "desc": "웅장한 오케스트라 사운드와 국내 최고 뮤지컬 배우들의 폭발적인 성량으로 가득 차는 대형 무대.", "tag": "감동 보장"}
        ]
    }
    
    # 필터링 로직 작동
    matched_artists = recommendations.get(user_genre, [])
    
    rec_col1, rec_col2 = st.columns(2)
    
    # 첫 번째 추천 아티스트
    with rec_col1:
        art1 = matched_artists[0]
        if art1["cost"] <= user_budget:
            st.markdown(f"""
            <div class="artist-card">
                <span style="background:#6366f1; color:#fff; font-size:0.75rem; padding:2px 8px; border-radius:20px; font-weight:bold;">{art1['tag']}</span>
                <h3 style="margin:8px 0 4px 0; color:#0f172a;">{art1['name']}</h3>
                <p style="font-size:0.85rem; color:#64748b; font-weight:600; margin-bottom:8px;">평균 예상 티켓가: ${art1['cost']}</p>
                <p style="font-size:0.9rem; color:#334155; line-height:1.4;">{art1['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"💡 예산 범위 내에 장르 매칭 아티스트({art1['name']}: ${art1['cost']})가 있으나 설정하신 예산 한도를 초과합니다.")

    # 두 번째 추천 아티스트
    with rec_col2:
        art2 = matched_artists[1]
        if art2["cost"] <= user_budget:
            st.markdown(f"""
            <div class="artist-card">
                <span style="background:#10b981; color:#fff; font-size:0.75rem; padding:2px 8px; border-radius:20px; font-weight:bold;">{art2['tag']}</span>
                <h3 style="margin:8px 0 4px 0; color:#0f172a;">{art2['name']}</h3>
                <p style="font-size:0.85rem; color:#64748b; font-weight:600; margin-bottom:8px;">평균 예상 티켓가: ${art2['cost']}</p>
                <p style="font-size:0.9rem; color:#334155; line-height:1.4;">{art2['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"💡 예산 범위 내에 장어 매칭 아티스트({art2['name']}: ${art2['cost']})가 있으나 설정하신 예산 한도를 초과합니다.")

    # ── 7. 미니 매거진 (다양한 볼거리 코너) ──────────────────────────
    st.write("")
    st.divider()
    st.markdown('<p class="section-lbl">05 — PERFORMANCE MAGAZINE</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">2026년 하반기 <em>주목해야 할</em> 해외 내한 빅이슈</p>', unsafe_allow_html=True)
    
    mag_c1, mag_c2, mag_c3 = st.columns(3)
    
    with mag_c1:
        st.markdown("""
        <div class="custom-card">
            <span style="color:#ef4444; font-size:0.75rem; font-weight:700; font-family:'IBM Plex Mono'">[ISSUE 01]</span>
            <h4 style="margin:6px 0; font-size:1.1rem; color:#0f172a;">콜드플레이(Coldplay) 스타디움 투어</h4>
            <p style="font-size:0.85rem; color:#64748b; margin-bottom:12px;">일정: 2026년 10월 예정</p>
            <p style="font-size:0.88rem; color:#475569; line-height:1.5;">지속 가능한 친환경 콘서트를 지향하는 콜드플레이가 역대급 LED 키네틱 레이저 연출과 자전거 발전기를 들고 한국을 다시 찾습니다. 주 경기장을 가득 채울 자일로밴드(LED 팔찌)의 물결을 미리 기대하세요.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with mag_c2:
        st.markdown("""
        <div class="custom-card">
            <span style="color:#2563eb; font-size:0.75rem; font-weight:700; font-family:'IBM Plex Mono'">[ISSUE 02]</span>
            <h4 style="margin:6px 0; font-size:1.1rem; color:#0f172a;">브루노 마스(Bruno Mars) 단독 내한 내정</h4>
            <p style="font-size:0.85rem; color:#64748b; margin-bottom:12px;">일정: 2026년 11월 예정</p>
            <p style="font-size:0.88rem; color:#475569; line-height:1.5;">최고의 팝스타 브루노 마스가 압도적인 소울과 펑크 밴드 세션들을 이끌고 한국 관객들을 찾아옵니다. 전 좌석 피켓팅이 예상되는 만큼 오픈 전 선예매 가이드를 눈여겨보는 것이 좋습니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with mag_c3:
        st.markdown("""
        <div class="custom-card">
            <span style="color:#10b981; font-size:0.75rem; font-weight:700; font-family:'IBM Plex Mono'">[ISSUE 03]</span>
            <h4 style="margin:6px 0; font-size:1.1rem; color:#0f172a;">그린데이(Green Day) 펑크록 헤드라이너</h4>
            <p style="font-size:0.85rem; color:#64748b; margin-bottom:12px;">일정: 2026년 12월 예정</p>
            <p style="font-size:0.88rem; color:#475569; line-height:1.5;">록 매니아들의 가슴을 뛰게 할 펑크록의 전설 그린데이가 페스티벌 단독 헤드라이너로 이름을 올렸습니다. 슬램과 에너제틱한 떼창이 준비된 관객이라면 놓쳐서는 안 될 올해의 마지막 빅카드입니다.</p>
        </div>
        """, unsafe_allow_html=True)
