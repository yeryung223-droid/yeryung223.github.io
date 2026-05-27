"""
Concert Ticket Analyzer — Survey Simulator
==========================================
실행 방법:
    pip install streamlit plotly pandas
    streamlit run concert_survey_app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="Concert Ticket Analyzer",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.main { background-color: #f7f5f0; }

/* 헤더 */
.app-header {
    background: #1a1a2e;
    padding: 1.2rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.app-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: white;
    margin: 0;
}
.app-title span { color: #ff4d1c; }

/* 섹션 타이틀 */
.sec-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff4d1c;
    margin-bottom: 0.3rem;
}
.sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #1a1a2e;
    margin-bottom: 1rem;
}

/* 스탯 카드 */
.stat-card {
    background: #1a1a2e;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
}
.stat-lbl {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-top: 0.2rem;
}

/* 결과 카드 */
.result-card {
    background: linear-gradient(135deg, #ff4d1c, #ff7a1a);
    border-radius: 16px;
    padding: 1.5rem;
    color: white;
}
.result-type {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}
.result-desc { font-size: 0.85rem; line-height: 1.6; opacity: 0.9; }

/* 인사이트 */
.insight-box {
    background: #1a1a2e;
    border-left: 4px solid #00b37e;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    color: rgba(255,255,255,0.8);
    font-size: 0.88rem;
    line-height: 1.6;
}
.insight-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00b37e;
    margin-bottom: 0.3rem;
}

/* 진행 바 텍스트 */
.progress-text {
    font-size: 0.7rem;
    font-weight: 600;
    color: #8a8780;
    text-align: right;
    margin-top: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# ── 기본 데이터 (5명 참여자) ──────────────────────────────────
BASE_DATA = pd.DataFrame([
    {"name": "P1", "age": "20대",   "freq": "자주",  "seat": "VIP",    "spend": 120, "sat": 5, "artist_priority": True},
    {"name": "P2", "age": "10대",   "freq": "가끔",  "seat": "저가",   "spend": 40,  "sat": 3, "artist_priority": False},
    {"name": "P3", "age": "30대+",  "freq": "거의 안 감", "seat": "중간", "spend": 80, "sat": 4, "artist_priority": True},
    {"name": "P4", "age": "20대",   "freq": "자주",  "seat": "VIP",    "spend": 150, "sat": 5, "artist_priority": True},
    {"name": "P5", "age": "10대",   "freq": "거의 안 감", "seat": "저가","spend": 30, "sat": 2, "artist_priority": False},
])

SPEND_MAP = {"$50 미만": 35, "$50–$100": 75, "$100 이상": 135}
SEAT_KO   = {"VIP": "VIP", "중간 좌석": "중간", "저가 좌석": "저가"}

# ── 세션 상태 초기화 ──────────────────────────────────────────
defaults = {
    "age": None, "freq": None, "factor": None,
    "spend_bucket": None, "seat": None, "sat": None,
    "artist_priority": None, "submitted": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── 헬퍼 함수 ────────────────────────────────────────────────
def get_pool() -> pd.DataFrame:
    """기본 데이터 + 현재 사용자 답변 병합"""
    pool = BASE_DATA.copy()
    me = {}
    if st.session_state.age:
        me["name"] = "나"
        me["age"]  = st.session_state.age
        me["freq"] = st.session_state.freq or "가끔"
        me["seat"] = SEAT_KO.get(st.session_state.seat, st.session_state.seat) if st.session_state.seat else None
        me["spend"]= SPEND_MAP.get(st.session_state.spend_bucket, 75) if st.session_state.spend_bucket else 75
        me["sat"]  = st.session_state.sat if st.session_state.sat else 3
        me["artist_priority"] = st.session_state.artist_priority if st.session_state.artist_priority is not None else False
        pool = pd.concat([pool, pd.DataFrame([me])], ignore_index=True)
    return pool

def answered_count() -> int:
    keys = ["age","freq","factor","spend_bucket","seat","sat","artist_priority"]
    return sum(1 for k in keys if st.session_state[k] is not None)

def get_audience_type():
    seat = st.session_state.seat or ""
    ap   = st.session_state.artist_priority
    freq = st.session_state.freq or ""
    factor = st.session_state.factor or ""

    if "VIP" in seat and ap:
        return "💎 헌신적 팬", (
            "아티스트에 대한 충성도가 높고 최고의 경험을 위해 기꺼이 투자하는 유형입니다. "
            "Pine & Gilmore의 경험 경제 이론에서 가장 높은 가치를 추구하는 관객군이며, "
            "샘플 데이터에서 이 유형의 평균 만족도는 5.0으로 최고입니다."
        )
    elif "저가" in seat:
        return "🎵 캐주얼 리스너", (
            "분위기와 음악 자체를 즐기는 유형입니다. 낮은 기대치가 오히려 만족도를 "
            "높이는 '기대치 효과'를 경험할 가능성이 있으며, 접근성을 중시합니다."
        )
    elif factor == "아티스트":
        return "🌟 아티스트 중심형", (
            "티켓 구매의 핵심 동기가 아티스트입니다. 연구 가설 C와 일치 — "
            "아티스트 인기가 가격·좌석보다 강한 구매 동인으로 작용하는 유형입니다."
        )
    elif freq == "자주":
        return "🎤 콘서트 매니아", (
            "반복 경험을 통해 콘서트 소비 패턴이 정교해진 유형입니다. "
            "가격 대비 가치 판단이 빠르고, 중간 좌석의 가성비를 잘 활용합니다."
        )
    else:
        return "🎶 균형 추구형", (
            "가격, 좌석, 경험을 균형 있게 고려하는 합리적 관객 유형입니다. "
            "중간 지출 + 중간 만족도 그룹에 해당합니다."
        )

def get_insight(pool: pd.DataFrame) -> str:
    seat  = st.session_state.seat or ""
    spend = st.session_state.spend_bucket or ""
    factor= st.session_state.factor or ""
    freq  = st.session_state.freq or ""
    done  = answered_count()

    if done == 0:
        return "아직 설문 참여 전입니다. 답변할수록 인사이트가 업데이트됩니다."
    if "VIP" in seat and spend == "$100 이상":
        return "VIP + 고지출 조합입니다. 현재 샘플에서 이 조합의 평균 만족도는 5.0 — 가장 높은 그룹입니다."
    if "저가" in seat and spend == "$50 미만":
        return "저가 좌석 + 낮은 지출 패턴입니다. 현재 데이터에서 이 그룹의 평균 만족도는 2.5로, 기대치 관리가 중요합니다."
    if factor == "아티스트":
        return "아티스트를 가장 중요하게 생각하는 관객은 팬 문화 연구에서 '충성 소비자'로 분류됩니다. 가격 저항이 낮은 경향이 있습니다."
    if freq == "자주":
        return "콘서트를 자주 가는 관객은 경험이 쌓이면서 가격 대비 가치 판단이 더 정교해지는 경향을 보입니다."
    return f"{done}개 답변 완료. 계속 답변하면 더 정확한 인사이트가 나타납니다!"

# ── 차트 함수 ─────────────────────────────────────────────────
CHART_BG    = "#1a1a2e"
CHART_PAPER = "#1a1a2e"
TEXT_COLOR  = "rgba(255,255,255,0.7)"
GRID_COLOR  = "rgba(255,255,255,0.08)"

def chart_defaults(fig):
    fig.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_PAPER,
        font=dict(color=TEXT_COLOR, family="Plus Jakarta Sans"),
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False,
    )
    return fig

def make_donut(pool: pd.DataFrame) -> go.Figure:
    counts = pool["seat"].value_counts().reindex(["VIP","중간","저가"], fill_value=0)
    colors = ["#ff4d1c","#f5a623","#00b37e"]
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color=CHART_BG, width=3)),
        textinfo="percent",
        textfont=dict(size=11, color="white"),
        hovertemplate="%{label}: %{value}명 (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_PAPER,
        font=dict(color=TEXT_COLOR, family="Plus Jakarta Sans"),
        margin=dict(l=0, r=0, t=10, b=10),
        showlegend=True,
        legend=dict(
            orientation="v", x=1.02, y=0.5,
            font=dict(size=11, color=TEXT_COLOR),
        ),
        annotations=[dict(
            text=f"<b>{len(pool)}</b><br>명",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="white"),
        )],
    )
    return fig

def make_spend_bar(pool: pd.DataFrame) -> go.Figure:
    age_order = ["10대", "20대", "30대+"]
    avg_spend = (
        pool.groupby("age")["spend"].mean()
        .reindex(age_order).fillna(0).round(0)
    )
    colors = ["#00b37e","#ff4d1c","#f5a623"]
    fig = go.Figure(go.Bar(
        x=avg_spend.values, y=avg_spend.index,
        orientation="h",
        marker=dict(color=colors[:len(avg_spend)], cornerradius=6),
        text=[f"${v:.0f}" for v in avg_spend.values],
        textposition="inside",
        textfont=dict(size=12, color="white", family="Plus Jakarta Sans"),
        hovertemplate="%{y}: $%{x:.0f}<extra></extra>",
    ))
    fig.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                     tickprefix="$", tickfont=dict(size=10))
    fig.update_yaxes(showgrid=False, tickfont=dict(size=12))
    return chart_defaults(fig)

def make_sat_scatter(pool: pd.DataFrame) -> go.Figure:
    p = pool.dropna(subset=["spend","sat"])
    color_map = {"VIP": "#ff4d1c", "중간": "#f5a623", "저가": "#00b37e", None: "#888"}
    colors = [color_map.get(s, "#888") for s in p["seat"]]
    symbols = ["나" if n == "나" else "●" for n in p["name"]]
    fig = go.Figure()
    for seat_type, color in color_map.items():
        if seat_type is None:
            continue
        sub = p[p["seat"] == seat_type]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["spend"], y=sub["sat"],
            mode="markers+text",
            name=seat_type,
            marker=dict(size=14, color=color, symbol="circle",
                        line=dict(color="white", width=1.5)),
            text=sub["name"],
            textposition="top center",
            textfont=dict(size=9, color="white"),
            hovertemplate="지출: $%{x}<br>만족도: %{y}/5<extra>" + (seat_type or "") + "</extra>",
        ))
    fig.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                     tickprefix="$", title_text="지출 금액",
                     title_font=dict(size=10), tickfont=dict(size=10))
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, range=[0.5, 5.5],
                     title_text="만족도", title_font=dict(size=10),
                     tickvals=[1,2,3,4,5], tickfont=dict(size=10))
    fig.update_layout(
        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_PAPER,
        font=dict(color=TEXT_COLOR, family="Plus Jakarta Sans"),
        margin=dict(l=10, r=10, t=10, b=30),
        showlegend=True,
        legend=dict(orientation="h", y=-0.25, font=dict(size=10, color=TEXT_COLOR)),
    )
    return fig

def make_factor_bar(pool: pd.DataFrame) -> go.Figure:
    """좌석 유형별 평균 만족도"""
    avg = (
        pool.groupby("seat")["sat"].mean()
        .reindex(["VIP","중간","저가"]).fillna(0).round(2)
    )
    colors = ["#ff4d1c","#f5a623","#00b37e"]
    fig = go.Figure(go.Bar(
        x=avg.index, y=avg.values,
        marker=dict(color=colors[:len(avg)], cornerradius=6),
        text=[f"{v:.1f}" for v in avg.values],
        textposition="outside",
        textfont=dict(size=13, color="white"),
        hovertemplate="%{x}: %{y:.2f}/5<extra></extra>",
    ))
    fig.update_xaxes(showgrid=False, tickfont=dict(size=12))
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR,
                     range=[0, 6], tickvals=[0,1,2,3,4,5],
                     tickfont=dict(size=10))
    return chart_defaults(fig)

# ═══════════════════════════════════════════════════════════════
#  UI
# ═══════════════════════════════════════════════════════════════

# 헤더
st.markdown("""
<div class="app-header">
  <p class="app-title">Concert<span>.</span>Survey Simulator</p>
  <p style="color:rgba(255,255,255,0.4);font-size:0.75rem;margin:0;">
      Audience Satisfaction Research · Yeryung Go · SKKU
  </p>
</div>
""", unsafe_allow_html=True)

# 레이아웃: 설문(왼) | 대시보드(오)
left, right = st.columns([1, 1.1], gap="large")

# ─────────────────────────────────────────────
#  왼쪽: 설문
# ─────────────────────────────────────────────
with left:
    st.markdown('<p class="sec-label">Survey Simulator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">당신은 어떤<br>콘서트 관객인가요?</p>', unsafe_allow_html=True)
    st.caption("7개 질문에 답하면 기존 참여자 5명 데이터와 합쳐져 결과가 실시간으로 업데이트됩니다.")

    # 진행률
    done = answered_count()
    st.progress(done / 7, text=f"{done} / 7 완료")

    st.divider()

    # ── Q1 연령대 ──
    with st.container(border=True):
        st.markdown("**Q1 / 7** &nbsp; 연령대가 어떻게 되세요?")
        age = st.radio("age_radio", ["10대 (Under 20)", "20대 (20–29)", "30대 이상 (30+)"],
                       index=None, label_visibility="collapsed", horizontal=True, key="age_radio")
        if age:
            map_age = {"10대 (Under 20)": "10대", "20대 (20–29)": "20대", "30대 이상 (30+)": "30대+"}
            st.session_state.age = map_age[age]

    # ── Q2 빈도 ──
    with st.container(border=True):
        st.markdown("**Q2 / 7** &nbsp; 콘서트에 얼마나 자주 가세요?")
        freq = st.radio("freq_radio", ["자주 간다", "가끔 간다", "거의 안 간다"],
                        index=None, label_visibility="collapsed", horizontal=True, key="freq_radio")
        if freq:
            map_freq = {"자주 간다": "자주", "가끔 간다": "가끔", "거의 안 간다": "거의 안 감"}
            st.session_state.freq = map_freq[freq]

    # ── Q3 중요 요소 ──
    with st.container(border=True):
        st.markdown("**Q3 / 7** &nbsp; 티켓 구매 시 가장 중요한 요소는?")
        factor = st.radio("factor_radio",
                          ["가격", "좌석 위치", "아티스트", "공연장", "굿즈/혜택"],
                          index=None, label_visibility="collapsed", horizontal=True, key="factor_radio")
        if factor:
            st.session_state.factor = factor

    # ── Q4 지출 ──
    with st.container(border=True):
        st.markdown("**Q4 / 7** &nbsp; 보통 콘서트 티켓에 얼마를 쓰세요?")
        spend = st.radio("spend_radio", ["$50 미만", "$50–$100", "$100 이상"],
                         index=None, label_visibility="collapsed", horizontal=True, key="spend_radio")
        if spend:
            st.session_state.spend_bucket = spend

    # ── Q5 좌석 ──
    with st.container(border=True):
        st.markdown("**Q5 / 7** &nbsp; 선호하는 좌석 구역은?")
        seat = st.radio("seat_radio", ["VIP", "중간 좌석", "저가 좌석"],
                        index=None, label_visibility="collapsed", horizontal=True, key="seat_radio")
        if seat:
            st.session_state.seat = seat

    # ── Q6 만족도 ──
    with st.container(border=True):
        st.markdown("**Q6 / 7** &nbsp; 콘서트 경험에 얼마나 만족하세요? (1–5)")
        sat = st.select_slider("sat_slider", options=[1, 2, 3, 4, 5],
                               value=None if not st.session_state.sat else st.session_state.sat,
                               label_visibility="collapsed", key="sat_slider",
                               format_func=lambda x: ["😞 매우 불만족","😐 불만족","😊 보통","😄 만족","🎉 매우 만족"][x-1])
        if sat:
            st.session_state.sat = sat

    # ── Q7 아티스트 ──
    with st.container(border=True):
        st.markdown("**Q7 / 7** &nbsp; 좋아하는 아티스트라면 비싼 티켓도 사겠어요?")
        ap = st.radio("ap_radio", ["Yes — 무조건 산다", "No — 가격이 중요하다"],
                      index=None, label_visibility="collapsed", horizontal=True, key="ap_radio")
        if ap:
            st.session_state.artist_priority = (ap == "Yes — 무조건 산다")

    st.divider()

    # ── 제출 / 초기화 버튼 ──
    col_a, col_b = st.columns(2)
    with col_a:
        if answered_count() == 7 and not st.session_state.submitted:
            if st.button("🎤 결과 보기", use_container_width=True, type="primary"):
                st.session_state.submitted = True
                st.rerun()
        elif st.session_state.submitted:
            st.success("✓ 제출 완료!")
    with col_b:
        if st.button("🔄 다시하기", use_container_width=True):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()

# ─────────────────────────────────────────────
#  오른쪽: 대시보드
# ─────────────────────────────────────────────
with right:
    pool = get_pool()

    st.markdown('<p class="sec-label">Live Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">실시간 결과</p>', unsafe_allow_html=True)

    # ── 스탯 카드 4개 ──
    s1, s2, s3, s4 = st.columns(4)
    avg_sat   = round(pool["sat"].mean(), 1)
    avg_spend = int(pool["spend"].mean())
    vip_pct   = int(len(pool[pool["seat"]=="VIP"]) / len(pool) * 100) if len(pool) > 0 else 0

    with s1:
        st.metric("👥 총 참여자", f"{len(pool)}명")
    with s2:
        st.metric("⭐ 평균 만족도", f"{avg_sat}/5")
    with s3:
        st.metric("💰 평균 지출", f"${avg_spend}")
    with s4:
        st.metric("💎 VIP 선호율", f"{vip_pct}%")

    st.divider()

    # ── 차트 행 1: 도넛 + 지출 바 ──
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🪑 좌석 선호도**")
        st.plotly_chart(make_donut(pool), use_container_width=True, key="donut")
    with c2:
        st.markdown("**💸 연령대별 평균 지출**")
        st.plotly_chart(make_spend_bar(pool), use_container_width=True, key="spend_bar")

    # ── 차트 행 2: 산점도 + 좌석별 만족도 ──
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**📊 지출 vs 만족도**")
        st.plotly_chart(make_sat_scatter(pool), use_container_width=True, key="scatter")
    with c4:
        st.markdown("**🏆 좌석 유형별 평균 만족도**")
        st.plotly_chart(make_factor_bar(pool), use_container_width=True, key="factor_bar")

    st.divider()

    # ── 제출 후: 관객 유형 결과 ──
    if st.session_state.submitted:
        atype, adesc = get_audience_type()
        st.markdown(f"""
        <div class="result-card">
            <p style="font-size:0.65rem;font-weight:700;letter-spacing:0.2em;
               text-transform:uppercase;color:rgba(255,255,255,0.7);margin-bottom:0.3rem;">
               당신의 관객 유형
            </p>
            <p class="result-type">{atype}</p>
            <p class="result-desc">{adesc}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")

    # ── 인사이트 박스 ──
    insight = get_insight(pool)
    st.markdown(f"""
    <div class="insight-box">
        <p class="insight-label">🔍 Live Insight</p>
        <p>{insight}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 원본 데이터 테이블 (토글) ──
    with st.expander("📋 전체 데이터 보기"):
        display_df = pool[["name","age","freq","seat","spend","sat"]].copy()
        display_df.columns = ["참여자","연령대","빈도","좌석","지출($)","만족도"]
        st.dataframe(
            display_df.style.background_gradient(subset=["만족도"], cmap="YlOrRd")
                            .background_gradient(subset=["지출($)"], cmap="Blues"),
            use_container_width=True, hide_index=True,
        )
