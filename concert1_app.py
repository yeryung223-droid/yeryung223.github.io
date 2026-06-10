"""
Concert Survey & Dashboard — Light Theme Version
================================================
실행: streamlit run concert_survey_app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── 1. 페이지 및 라이트 테마 설정 ──────────────────────────────
st.set_page_config(
    page_title="Concert Audience Survey",
    page_icon="📊",
    layout="wide",
)

# 화이트 & 블루 & 소프트 레드 기반의 밝은 테마 CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

/* 전체 배경 및 폰트 */
html, body, [class*="css"] { 
    font-family: 'Pretendard', sans-serif; 
    background-color: #f8fafc !important; 
    color: #1e293b; 
}
.stApp { background-color: #f8fafc !important; }

/* 섹션 레이블 및 타이틀 */
.section-lbl {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #6366f1; margin-bottom: 0.4rem;
}
.section-ttl {
    font-size: 2rem; font-weight: 700; color: #0f172a; line-height: 1.2; margin-bottom: 1.5rem;
}
.section-ttl em { color: #ef4444; font-style: normal; }

/* 커스텀 카드 디자인 (밝은 배경 + 부드러운 그림자) */
.custom-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 1.8rem; margin-bottom: 1rem; height: 100%;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

/* 설문 폼 헤더 */
.survey-header {
    background: linear-gradient(135deg, #f1f5f9, #ffffff);
    border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;
}

/* Metric 스타일 */
[data-testid="metric-container"] {
    background: #ffffff !important; border: 1px solid #e2e8f0 !important; 
    border-radius: 12px !important; padding: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; font-weight: 600; }
[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 700; }

/* 탭 스타일 */
.stTabs [data-baseweb="tab-list"] { background-color: transparent; }
.stTabs [data-baseweb="tab"] { color: #64748b; font-weight: 600; }
.stTabs [aria-selected="true"] { color: #6366f1 !important; border-bottom-color: #6366f1 !important; }

</style>
""", unsafe_allow_html=True)


# ── 2. 가상 데이터베이스 초기화 (Session State) ──────────────────
if "survey_db" not in st.session_state:
    st.session_state.survey_db = pd.DataFrame([
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 150, "sat": 5},
        {"age": "20대", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 95, "sat": 4},
        {"age": "10대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 45, "sat": 3},
        {"age": "30대 이상", "freq": "거의 안 간다", "seat": "중간 좌석", "spend": 80, "sat": 3},
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 190, "sat": 5},
    ])


# ── 3. 헤더 영역 ─────────────────────────────────────────────
st.markdown("""
<div style="background:#ffffff; border-bottom:1px solid #e2e8f0; padding:1rem 2rem; display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem;">
  <span style="font-family:'IBM Plex Mono',monospace; font-size:1.2rem; font-weight:700; color:#6366f1; letter-spacing:-0.02em;">
    CONCERT<span style="color:#0f172a;">.</span>SURVEY<span style="color:#94a3b8; font-weight:300;">_INSIGHT</span>
  </span>
  <span style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#64748b; letter-spacing:0.1em;">
    AUDIENCE EXPERIENCE RESEARCH · 2026
  </span>
</div>
""", unsafe_allow_html=True)


# ── 4. 입력 섹션 (2컬럼 레이아웃) ──────────────────────────────
col_input, col_recent = st.columns([1.2, 1], gap="large")

with col_input:
    st.markdown('<p class="section-lbl">01 — COLLECT</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">관객 <em>경험</em> 설문</p>', unsafe_allow_html=True)
    
    with st.form(key="light_survey_form", clear_on_submit=True):
        st.markdown("""
        <div class="survey-header">
            <span style="color:#6366f1; font-weight:700; font-size:0.9rem;">참여 안내</span>
            <p style="font-size:0.85rem; color:#475569; margin-top:4px;">콘서트 관람에 대한 본인의 실제 경험을 바탕으로 답변해 주세요.</p>
        </div>
        """, unsafe_allow_html=True)
        
        q1 = st.segmented_control("Q1. 연령대", ["10대", "20대", "30대 이상"], default="20대")
        st.write("")
        q2 = st.selectbox("Q2. 공연 관람 빈도", ["자주 간다", "가끔 간다", "거의 안 간다"])
        st.write("")
        q3 = st.radio("Q3. 주로 이용하는 좌석", ["VIP 좌석", "중간 좌석", "저가 좌석"], horizontal=True)
        st.write("")
        q4 = st.slider("Q4. 평균 티켓 지출 ($)", 0, 300, 100, step=5)
        st.write("")
        q5 = st.select_slider("Q5. 관람 만족도 (1~5)", options=[1, 2, 3, 4, 5], value=4)
        
        st.write("")
        submit = st.form_submit_button("✅ 설문 제출하기")
        
        if submit:
            new_row = pd.DataFrame([{"age": q1, "freq": q2, "seat": q3, "spend": q4, "sat": q5}])
            st.session_state.survey_db = pd.concat([st.session_state.survey_db, new_row], ignore_index=True)
            st.toast("데이터가 반영되었습니다!", icon="🚀")
            st.rerun()

with col_recent:
    st.markdown('<p class="section-lbl">02 — LOGS</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">최근 <em>응답</em> 현황</p>', unsafe_allow_html=True)
    
    data_log = st.session_state.survey_db.iloc[::-1].copy()
    data_log.columns = ["연령대", "빈도", "좌석", "지출($)", "만족도"]
    
    # matplotlib이 설치되어 있다면 그라데이션 적용, 없다면 기본 표 출력
    try:
        st.dataframe(
            data_log.style.background_gradient(subset=["만족도"], cmap="YlGnBu")
                          .background_gradient(subset=["지출($)"], cmap="Purples"),
            use_container_width=True, height=450
        )
    except:
        st.dataframe(data_log, use_container_width=True, height=450)


# ── 5. 대시보드 섹션 ──────────────────────────────────────────
st.divider()
st.markdown('<p class="section-lbl">03 — ANALYTICS</p>', unsafe_allow_html=True)
st.markdown('<p class="section-ttl">데이터 <em>실시간</em> 분석</p>', unsafe_allow_html=True)

df = st.session_state.survey_db

# 핵심 지표 Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("총 응답수", f"{len(df)}건")
m2.metric("평균 지출액", f"${df['spend'].mean():.1f}")
m3.metric("평균 만족도", f"{df['sat'].mean():.2f}")
m4.metric("VIP 선호도", f"{(len(df[df['seat']=='VIP 좌석'])/len(df)*100):.1f}%")

st.write("")

# 라이트 모드용 차트 설정
CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#1e293b", family="Pretendard"),
    margin=dict(l=20, r=20, t=40, b=20)
)
GRID_STYLE = dict(gridcolor="#e2e8f0", zeroline=False)

c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='custom-card'><strong>🪑 좌석별 선호 비율</strong>", unsafe_allow_html=True)
    seat_val = df["seat"].value_counts()
    fig1 = go.Figure(go.Pie(
        labels=seat_val.index, values=seat_val.values, hole=0.6,
        marker=dict(colors=["#6366f1", "#8b5cf6", "#ec4899"])
    ))
    fig1.update_layout(**CHART_THEME, height=300, showlegend=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='custom-card'><strong>💰 지출 vs 만족도 상관관계</strong>", unsafe_allow_html=True)
    fig2 = go.Figure(go.Scatter(
        x=df["spend"], y=df["sat"], mode="markers",
        marker=dict(size=12, color="#6366f1", opacity=0.6, line=dict(width=1, color="white"))
    ))
    fig2.update_layout(**CHART_THEME, height=300)
    fig2.update_xaxes(title="지출 금액 ($)", **GRID_STYLE)
    fig2.update_yaxes(title="만족도", **GRID_STYLE, tickvals=[1,2,3,4,5])
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown("<div class='custom-card'><strong>📊 연령대별 평균 지출액</strong>", unsafe_allow_html=True)
    age_avg = df.groupby("age")["spend"].mean().reindex(["10대", "20대", "30대 이상"]).fillna(0)
    fig3 = go.Figure(go.Bar(
        x=age_avg.index, y=age_avg.values,
        marker=dict(color="#6366f1", cornerradius=8),
        text=[f"${v:.0f}" for v in age_avg.values], textposition="auto"
    ))
    fig3.update_layout(**CHART_THEME, height=300)
    fig3.update_yaxes(**GRID_STYLE)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div class='custom-card'><strong>📈 관람 빈도 현황</strong>", unsafe_allow_html=True)
    freq_val = df["freq"].value_counts().reindex(["자주 간다", "가끔 간다", "거의 안 간다"]).fillna(0)
    fig4 = go.Figure(go.Bar(
        x=freq_counts.index if 'freq_counts' in locals() else freq_val.index, 
        y=freq_counts.values if 'freq_counts' in locals() else freq_val.values,
        marker=dict(color="#ef4444", cornerradius=8)
    ))
    fig4.update_layout(**CHART_THEME, height=300)
    fig4.update_yaxes(**GRID_STYLE)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
