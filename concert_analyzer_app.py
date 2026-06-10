"""
Concert Ticket Analyzer — Streamlit App
========================================
실행:
    pip install streamlit plotly pandas
    streamlit run concert_analyzer_app.py
"""
 
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
 
# ── 페이지 설정 ───────────────────────────────────────────────
st.set_page_config(
    page_title="Concert Ticket Analyzer",
    page_icon="🎤",
    layout="wide",
)
 
# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');
 
html, body, [class*="css"] { font-family:'Lora',Georgia,serif; }
.stApp, .stMainBlockContainer { background:#07080a !important; color:#f0ece4; }
section[data-testid="stSidebar"] { background:#0f1014 !important; }
 
/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background:#0f1014; border-radius:10px;
    padding:.3rem; gap:.2rem; border:1px solid #1e1e26;
}
.stTabs [data-baseweb="tab"] {
    font-family:'IBM Plex Mono',monospace;
    font-size:.62rem; letter-spacing:.15em; text-transform:uppercase;
    color:#6b6878 !important; border-radius:7px; padding:.45rem .9rem;
}
.stTabs [aria-selected="true"] {
    background:#e84545 !important; color:#fff !important;
}
 
/* 공통 컴포넌트 */
.lbl {
    font-family:'IBM Plex Mono',monospace;
    font-size:.6rem; letter-spacing:.35em; text-transform:uppercase;
    color:#e84545; margin-bottom:.25rem;
}
.ttl {
    font-size:2rem; font-weight:600; color:#f0ece4;
    line-height:1.1; margin-bottom:1rem;
}
.ttl em { color:#f5a623; font-style:normal; }
 
/* 히어로 */
.hero {
    background:linear-gradient(135deg,#0f1014,#07080a);
    border:1px solid #1e1e26; border-radius:16px;
    padding:2.5rem 3rem; margin-bottom:1.5rem;
}
.hero-eyebrow {
    font-family:'IBM Plex Mono',monospace;
    font-size:.6rem; letter-spacing:.38em; text-transform:uppercase;
    color:#e84545; margin-bottom:.8rem;
}
.hero-h1 {
    font-size:clamp(2.2rem,5vw,4.5rem);
    font-weight:600; line-height:.95; margin-bottom:1rem; color:#f0ece4;
}
.hero-h1 .r{color:#e84545;} .hero-h1 .a{color:#f5a623;display:block;}
.hero-sub { font-size:.95rem; font-style:italic; color:#6b6878; line-height:1.7; max-width:500px; }
 
/* 카드들 */
.card {
    background:#0f1014; border:1px solid #1e1e26;
    border-radius:12px; padding:1.5rem; height:100%;
}
.card-icon {
    font-family:'IBM Plex Mono',monospace; font-size:1.6rem;
    color:#f5a623; margin-bottom:.7rem; opacity:.75; font-weight:700;
}
.card h3 { font-size:1rem; color:#f0ece4; margin-bottom:.4rem; }
.card p  { font-size:.86rem; color:#6b6878; line-height:1.75; margin:0; }
.card p strong { color:#f0ece4; }
 
/* 인사이트 */
.ins {
    background:#0f1014; border-left:3px solid #3ecf8e;
    border-radius:0 10px 10px 0; padding:.9rem 1.2rem; margin-bottom:.7rem;
}
.ins-lbl {
    font-family:'IBM Plex Mono',monospace; font-size:.56rem;
    letter-spacing:.22em; text-transform:uppercase; color:#3ecf8e; margin-bottom:.25rem;
}
.ins p { font-size:.84rem; color:#6b6878; line-height:1.65; margin:0; }
.ins p strong { color:#f0ece4; }
 
/* Purpose */
.pur {
    display:flex; gap:1.4rem; padding:1.4rem 0;
    border-bottom:1px solid #1e1e26; align-items:flex-start;
}
.pur-n { font-size:3rem; font-weight:600; color:#1e1e26; line-height:1; flex-shrink:0; width:50px; }
.pur h3 { font-size:1rem; color:#f0ece4; margin-bottom:.35rem; }
.pur p  { font-size:.86rem; color:#6b6878; line-height:1.75; margin:0; }
 
/* Q 카드 */
.qc {
    background:#0f1014; border:1px solid #1e1e26;
    border-radius:12px; padding:1.4rem 1.4rem 1rem; position:relative; margin-bottom:.7rem;
}
.qc-n {
    font-size:3.5rem; font-weight:600; color:#1e1e26;
    position:absolute; top:.2rem; right:.8rem; line-height:1;
}
.qc p     { font-size:.97rem; font-style:italic; color:#f0ece4; position:relative; z-index:1; margin:0; }
.qc .sub  { font-size:.78rem; color:#6b6878; font-style:normal; margin-top:.35rem; }
 
/* Method */
.mth {
    background:#0f1014; border:1px solid #1e1e26;
    border-radius:12px; padding:1.4rem;
}
.mth-ttl {
    font-family:'IBM Plex Mono',monospace; font-size:.58rem;
    letter-spacing:.26em; text-transform:uppercase; color:#f5a623;
    padding-bottom:.6rem; border-bottom:1px solid #1e1e26; margin-bottom:.9rem;
}
.mth li { font-size:.86rem; color:#6b6878; margin-bottom:.35rem; line-height:1.55; }
 
/* Exp 카드 */
.exc {
    background:#0f1014; border:1px solid #1e1e26;
    border-radius:12px; padding:1.5rem; margin-bottom:.7rem;
}
.exc-icon {
    font-family:'IBM Plex Mono',monospace; font-size:.58rem;
    letter-spacing:.26em; text-transform:uppercase; color:#3ecf8e; margin-bottom:.6rem;
}
.exc h3 { font-size:1rem; color:#f0ece4; margin-bottom:.4rem; }
.exc p  { font-size:.86rem; color:#6b6878; line-height:1.75; margin:0; }
 
/* 결론 */
.conc-big { font-size:clamp(2rem,5vw,4rem); font-weight:600; line-height:1; color:#f0ece4; }
.conc-big .r{color:#e84545;} .conc-big .a{color:#f5a623;}
.conc-body p { font-size:.93rem; color:#6b6878; line-height:1.85; margin-bottom:.9rem; }
.conc-body p strong { color:#f0ece4; }
.conc-credit {
    font-family:'IBM Plex Mono',monospace; font-size:.62rem;
    letter-spacing:.16em; text-transform:uppercase; color:#3a3a48;
    margin-top:1.2rem; padding-top:.9rem; border-top:1px solid #1e1e26;
}
.conc-credit em { color:#f5a623; font-style:normal; }
 
/* Survey Q */
.sq {
    background:#0f1014; border:1px solid #1e1e26;
    border-radius:10px; padding:1.2rem 1.5rem; margin-bottom:.6rem;
}
.sq-n { font-family:'IBM Plex Mono',monospace; font-size:1.4rem; color:#e84545; font-weight:700; }
.sq-txt { font-size:.97rem; color:#f0ece4; margin:.3rem 0 .7rem; }
.pill {
    display:inline-block; border:1px solid #1e1e26;
    border-radius:6px; padding:.2rem .65rem;
    font-family:'IBM Plex Mono',monospace; font-size:.62rem;
    letter-spacing:.1em; color:#6b6878; margin:.2rem .3rem .2rem 0;
}
 
/* Metric */
[data-testid="metric-container"] {
    background:#0f1014 !important; border:1px solid #1e1e26 !important;
    border-radius:10px !important;
}
[data-testid="stMetricLabel"]  { color:#6b6878 !important; }
[data-testid="stMetricValue"]  { color:#f0ece4 !important; }
[data-testid="stMetricDelta"]  { font-size:.72rem !important; }
hr { border-color:#1e1e26 !important; }
</style>
""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
#  데이터 (20명 — 2025 공연시장 보고서 기반)
# ══════════════════════════════════════════════════════════════
DF = pd.DataFrame([
    {"id":"P01","age":"20대","freq":"자주",       "seat":"VIP", "spend":140,"sat":5},
    {"id":"P02","age":"20대","freq":"자주",       "seat":"VIP", "spend":155,"sat":5},
    {"id":"P03","age":"20대","freq":"자주",       "seat":"VIP", "spend":180,"sat":5},
    {"id":"P04","age":"20대","freq":"자주",       "seat":"중간","spend":100,"sat":4},
    {"id":"P05","age":"20대","freq":"자주",       "seat":"VIP", "spend":160,"sat":5},
    {"id":"P06","age":"20대","freq":"가끔",       "seat":"중간","spend":85, "sat":4},
    {"id":"P07","age":"20대","freq":"가끔",       "seat":"중간","spend":75, "sat":4},
    {"id":"P08","age":"20대","freq":"가끔",       "seat":"저가","spend":45, "sat":3},
    {"id":"P09","age":"10대","freq":"가끔",       "seat":"저가","spend":38, "sat":3},
    {"id":"P10","age":"10대","freq":"가끔",       "seat":"저가","spend":42, "sat":3},
    {"id":"P11","age":"10대","freq":"거의 안 감", "seat":"저가","spend":30, "sat":2},
    {"id":"P12","age":"10대","freq":"거의 안 감", "seat":"저가","spend":25, "sat":2},
    {"id":"P13","age":"30대+","freq":"가끔",      "seat":"중간","spend":90, "sat":4},
    {"id":"P14","age":"30대+","freq":"가끔",      "seat":"중간","spend":95, "sat":4},
    {"id":"P15","age":"30대+","freq":"자주",      "seat":"VIP", "spend":150,"sat":5},
    {"id":"P16","age":"30대+","freq":"거의 안 감","seat":"중간","spend":70, "sat":3},
    {"id":"P17","age":"20대","freq":"거의 안 감", "seat":"저가","spend":35, "sat":3},
    {"id":"P18","age":"30대+","freq":"거의 안 감","seat":"저가","spend":40, "sat":2},
    {"id":"P19","age":"10대","freq":"자주",       "seat":"중간","spend":55, "sat":4},
    {"id":"P20","age":"30대+","freq":"자주",      "seat":"VIP", "spend":170,"sat":5},
])
 
# ══════════════════════════════════════════════════════════════
#  차트 함수
# ══════════════════════════════════════════════════════════════
BG = "#07080a"; PAPER = "#07080a"
TX = "rgba(240,236,228,.72)"; GR = "rgba(255,255,255,.06)"
FONT = "IBM Plex Mono"
RED, AMB, GRN = "#e84545", "#f5a623", "#3ecf8e"
 
def _base(fig, **kw):
    fig.update_layout(
        plot_bgcolor=BG, paper_bgcolor=PAPER,
        font=dict(color=TX, family=FONT),
        margin=dict(l=8,r=8,t=28,b=8),
        showlegend=False, **kw)
    return fig
 
def ch_donut(df):
    c = df["seat"].value_counts().reindex(["VIP","중간","저가"], fill_value=0)
    fig = go.Figure(go.Pie(
        labels=c.index, values=c.values, hole=.6,
        marker=dict(colors=[RED,AMB,GRN], line=dict(color=BG,width=3)),
        textinfo="percent+label", textfont=dict(size=11,color="#fff"),
        hovertemplate="%{label}: %{value}명 (%{percent})<extra></extra>"))
    fig.update_layout(plot_bgcolor=BG, paper_bgcolor=PAPER,
        font=dict(color=TX,family=FONT), margin=dict(l=0,r=0,t=8,b=8),
        showlegend=False,
        annotations=[dict(text=f"<b>{len(df)}</b><br>명",x=.5,y=.5,
            showarrow=False,font=dict(size=13,color="#fff"))])
    return fig
 
def ch_spend(df):
    avg = df.groupby("age")["spend"].mean().reindex(["10대","20대","30대+"]).fillna(0).round(0)
    fig = go.Figure(go.Bar(
        x=avg.values, y=avg.index, orientation="h",
        marker=dict(color=[GRN,RED,AMB], cornerradius=5),
        text=[f"${v:.0f}" for v in avg.values], textposition="inside",
        textfont=dict(size=12,color="#fff"),
        hovertemplate="%{y}: $%{x:.0f}<extra></extra>"))
    fig.update_xaxes(showgrid=True,gridcolor=GR,zeroline=False,tickprefix="$",tickfont=dict(size=10))
    fig.update_yaxes(showgrid=False,tickfont=dict(size=11))
    return _base(fig)
 
def ch_scatter(df):
    cmap = {"VIP":RED,"중간":AMB,"저가":GRN}
    p = df.dropna(subset=["spend","sat"])
    fig = go.Figure()
    for seat,color in cmap.items():
        s = p[p["seat"]==seat]
        if s.empty: continue
        fig.add_trace(go.Scatter(
            x=s["spend"], y=s["sat"], mode="markers+text", name=seat,
            marker=dict(size=13,color=color,line=dict(color="#fff",width=1.5)),
            text=s["id"], textposition="top center",
            textfont=dict(size=8,color="#fff"),
            hovertemplate="$%{x} · 만족도 %{y}<extra>"+seat+"</extra>"))
    fig.update_xaxes(showgrid=True,gridcolor=GR,zeroline=False,
        tickprefix="$",title_text="지출",title_font=dict(size=10),tickfont=dict(size=10))
    fig.update_yaxes(showgrid=True,gridcolor=GR,range=[.5,5.5],
        title_text="만족도",tickvals=[1,2,3,4,5],tickfont=dict(size=10))
    return _base(fig, showlegend=True,
        legend=dict(orientation="h",y=-.28,font=dict(size=10,color=TX)))
 
def ch_seat_sat(df):
    avg = df.groupby("seat")["sat"].mean().reindex(["VIP","중간","저가"]).fillna(0).round(2)
    fig = go.Figure(go.Bar(
        x=avg.index, y=avg.values,
        marker=dict(color=[RED,AMB,GRN], cornerradius=5),
        text=[f"{v:.1f}" for v in avg.values], textposition="outside",
        textfont=dict(size=13,color="#fff"),
        hovertemplate="%{x}: %{y:.2f}/5<extra></extra>"))
    fig.update_xaxes(showgrid=False,tickfont=dict(size=12))
    fig.update_yaxes(showgrid=True,gridcolor=GR,range=[0,6],tickvals=[0,1,2,3,4,5],tickfont=dict(size=10))
    return _base(fig)
 
def ch_freq(df):
    c = df["freq"].value_counts().reindex(["자주","가끔","거의 안 감"],fill_value=0)
    fig = go.Figure(go.Bar(
        x=c.index, y=c.values,
        marker=dict(color=[RED,AMB,GRN],cornerradius=5),
        text=c.values, textposition="outside",
        textfont=dict(size=13,color="#fff"),
        hovertemplate="%{x}: %{y}명<extra></extra>"))
    fig.update_xaxes(showgrid=False,tickfont=dict(size=12))
    fig.update_yaxes(showgrid=True,gridcolor=GR,tickfont=dict(size=10))
    return _base(fig)
 
def ch_hist(df):
    p = df.dropna(subset=["sat"])
    fig = go.Figure(go.Histogram(
        x=p["sat"], nbinsx=5,
        marker=dict(color=RED,cornerradius=5,line=dict(color=BG,width=2)),
        hovertemplate="만족도 %{x}: %{y}명<extra></extra>"))
    fig.update_xaxes(tickvals=[1,2,3,4,5],tickfont=dict(size=11))
    fig.update_yaxes(showgrid=True,gridcolor=GR,tickfont=dict(size=10))
    return _base(fig)
 
# ══════════════════════════════════════════════════════════════
#  헤더
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:#0f1014;border:1px solid #1e1e26;border-radius:12px;
     padding:.9rem 1.8rem;display:flex;justify-content:space-between;
     align-items:center;margin-bottom:1.2rem;">
  <span style="font-family:'IBM Plex Mono',monospace;font-size:1rem;
        font-weight:700;color:#e84545;letter-spacing:.06em;">
    Concert<span style="color:#f0ece4;">.</span>Analyzer
  </span>
  <span style="font-family:'IBM Plex Mono',monospace;font-size:.6rem;
        letter-spacing:.2em;text-transform:uppercase;color:#3a3a48;">
    Yeryung Go · Korea Dance · SKKU · 2025
  </span>
</div>
""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
#  탭 네비게이션
# ══════════════════════════════════════════════════════════════
tabs = st.tabs([
    "01 · Intro",
    "02 · Background",
    "03 · Purpose",
    "04 · Questions",
    "05 · Method",
    "06 · Survey",
    "07 · Data",
    "08 · Expected",
    "09 · Conclusion",
])
 
# ══════════════════════════════════════════════════════════════
#  01 — INTRODUCTION
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
    <div class="hero">
      <p class="hero-eyebrow">Research Project · Audience Satisfaction Study · 2025</p>
      <p class="hero-h1">Concert <span class="r">Ticket</span><span class="a">Analyzer</span></p>
      <p class="hero-sub">콘서트 티켓 가격, 좌석, 팬 문화가 관람 경험을 어떻게 형성하는가 —
      그리고 지불한 금액이 느끼는 감정을 바꾸는가.</p>
    </div>
    """, unsafe_allow_html=True)
 
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("👥 참여자",      "20명")
    with c2: st.metric("📋 설문 문항",   "7개")
    with c3: st.metric("📈 시장 성장률", "+18.8%")
    with c4: st.metric("🎭 관람률",      "60.2%", "-2.8%p", delta_color="inverse")
 
    st.divider()
    col_l, col_r = st.columns([1.1,1], gap="large")
    with col_l:
        st.markdown('<p class="lbl">01 — Introduction</p>', unsafe_allow_html=True)
        st.markdown('<p class="ttl">Why concerts <em>matter</em></p>', unsafe_allow_html=True)
        st.markdown("""
        라이브 콘서트는 **단 한 번뿐인 사건**입니다. 스트리밍과 달리 날짜를 정하고,
        티켓을 구매하고, 공연장으로 이동하는 헌신을 요구합니다.
        그 투자는 첫 음이 울리기 훨씬 전부터 시작됩니다.
 
        최근 **다이나믹 프라이싱** 도입으로 같은 공연의 VIP석은 $300 이상,
        저가석은 $40 — 어디에 앉느냐가 어떻게 느끼느냐를 바꾸는가?
        이것이 이 연구의 핵심 질문입니다.
        """)
        st.markdown("""
        <div class="ins">
          <p class="ins-lbl">핵심 질문</p>
          <p><strong>"Does where you sit change how you feel?"</strong><br>
          좌석 위치가 만족도를 결정하는가, 아니면 아티스트에 대한 감정이 더 큰 변수인가.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.markdown("""
        <div class="card" style="margin-top:3rem;">
          <div style="font-family:'IBM Plex Mono',monospace;">
            <div style="font-size:.55rem;letter-spacing:.22em;text-transform:uppercase;color:#6b6878;">Event</div>
            <div style="font-size:1.1rem;color:#f0ece4;margin-bottom:.8rem;">★ Live Concert 2025</div>
            <hr style="border-color:#1e1e26;margin:.7rem 0;"/>
            <div style="display:flex;justify-content:space-between;margin-bottom:.5rem;">
              <div>
                <div style="font-size:.52rem;color:#6b6878;letter-spacing:.18em;text-transform:uppercase;">Section</div>
                <div style="color:#f0ece4;">VIP · Row A</div>
              </div>
              <div>
                <div style="font-size:.52rem;color:#6b6878;letter-spacing:.18em;text-transform:uppercase;">Date</div>
                <div style="color:#f0ece4;">SAT · NOV 2025</div>
              </div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:.7rem;">
              <div>
                <div style="font-size:.52rem;color:#6b6878;letter-spacing:.18em;text-transform:uppercase;">Face Value</div>
                <div style="font-size:2.2rem;color:#e84545;line-height:1;">$160</div>
              </div>
              <div style="text-align:right;">
                <div style="font-size:.52rem;color:#6b6878;letter-spacing:.18em;text-transform:uppercase;">Satisfaction</div>
                <div style="font-size:2.2rem;color:#3ecf8e;line-height:1;">5 / 5</div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
#  02 — BACKGROUND
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="lbl">02 — Research Background</p>', unsafe_allow_html=True)
    st.markdown('<p class="ttl">The <em>landscape</em></p>', unsafe_allow_html=True)
 
    c1,c2,c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown("""<div class="card">
          <div class="card-icon">1.7조</div>
          <h3>국내 공연시장 2025</h3>
          <p>2025년 국내 공연 티켓 판매액 <strong>1조 7326억원</strong>, 전년 대비 +18.8%.
          공연 건수(+9.6%)·회차(+11.3%)·예매 수(+10.8%) 모두 증가했으나,
          직접 관람률은 오히려 2.8%p 하락. <em style="font-size:.75rem;color:#3a3a48;">
          출처: 문화체육관광부·예술경영지원센터, 2026.03</em></p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card">
          <div class="card-icon">K-POP</div>
          <h3>팬덤 소비가 시장을 키운다</h3>
          <p>대중음악 티켓 판매액 <strong>9817억원(+29%)</strong>. 1만석 이상 초대형 공연이
          잇따르며 평균 단가도 상승. 고가 티켓·반복 관람에 나서는 팬층이 매출을 견인하는 반면,
          신규 유입 관람층은 거의 늘지 않는 구조.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card">
          <div class="card-icon">EXP</div>
          <h3>공연은 '작은 여행'이 됐다</h3>
          <p>타 지역 공연 이동 시 관광 관련 지출 <strong>+30%</strong>,
          같은 지역도 외식·쇼핑 지출 <strong>+36%</strong> 증가.
          Pine &amp; Gilmore의 경험 경제 이론처럼 관객은 단순 공연이 아닌
          <em>하루 전체의 경험</em>을 구매하고 있다.</p>
        </div>""", unsafe_allow_html=True)
 
    st.divider()
    m1,m2,m3,m4 = st.columns(4)
    with m1: st.metric("🎫 티켓 예매 수",  "2,478만 매", "+10.8%")
    with m2: st.metric("🎤 대중음악 매출", "9,817억원",  "+29.0%")
    with m3: st.metric("👥 직접 관람률",   "60.2%",       "-2.8%p", delta_color="inverse")
    with m4: st.metric("💃 무용 매출",     "267억원",     "+29.5%")
 
# ══════════════════════════════════════════════════════════════
#  03 — PURPOSE
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="lbl">03 — Research Purpose</p>', unsafe_allow_html=True)
    st.markdown('<p class="ttl">What we <em>aim</em> to find</p>', unsafe_allow_html=True)
 
    for n, h, b in [
        ("01","구매 행동 분석 (Analyze Purchasing Behavior)",
         "관객이 어떤 티켓을 살지 결정하는 과정을 매핑합니다. 가격·좌석 가용성·또래 영향력의 역할을 살펴보고, 구매가 신중한 선택인지 감정적 충동인지를 파악합니다."),
        ("02","만족도 요인 식별 (Identify Satisfaction Factors)",
         "좌석 근접성·음향·공연 분위기·아티스트 교감·굿즈 중 만족도와 가장 강하게 상관된 요소를 찾습니다. 사전 기대와 실제 경험을 구분합니다."),
        ("03","가격·좌석·경험 비교 (Compare Price, Seating & Experience)",
         "더 많이 쓴 관객이 더 높은 만족도를 보고하는지, 특정 가격 임계점에서 수확체감이 나타나는지를 검증합니다."),
    ]:
        st.markdown(f"""
        <div class="pur">
          <div class="pur-n">{n}</div>
          <div>
            <h3>{h}</h3>
            <p>{b}</p>
          </div>
        </div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
#  04 — RESEARCH QUESTIONS
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="lbl">04 — Research Questions</p>', unsafe_allow_html=True)
    st.markdown('<p class="ttl">Core <em>questions</em></p>', unsafe_allow_html=True)
 
    qa = [
        ("01","티켓 구매 시 가장 중요한 요소는 무엇인가?",
         "Price · Seat · Artist · Venue · Merchandise — which wins?"),
        ("02","저가 티켓 vs 좋은 좌석, 어느 쪽을 선호하는가?",
         "The price-proximity trade-off at the heart of ticket purchasing."),
        ("03","티켓 가격이 만족도에 어떤 영향을 미치는가?",
         "Does spending more raise expectations — and does reality meet them?"),
        ("04","콘서트 참여 빈도가 구매 패턴에 영향을 주는가?",
         "Frequency shapes preferences — do regular attendees think differently?"),
    ]
    col1, col2 = st.columns(2, gap="medium")
    for i,(n,q,s) in enumerate(qa):
        with (col1 if i%2==0 else col2):
            st.markdown(f"""
            <div class="qc">
              <div class="qc-n">{n}</div>
              <p>{q}</p>
              <p class="sub">{s}</p>
            </div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
#  05 — METHOD
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<p class="lbl">05 — Research Method</p>', unsafe_allow_html=True)
    st.markdown('<p class="ttl">How we <em>collect</em> data</p>', unsafe_allow_html=True)
 
    m1,m2,m3 = st.columns(3, gap="medium")
    with m1:
        st.markdown("""<div class="mth">
          <div class="mth-ttl">Participants</div>
          <ul>
            <li>→ 10~30대 청소년 및 젊은 성인</li>
            <li>→ 콘서트 경험 1회 이상</li>
            <li>→ 음악·공연에 관심 있는 학생</li>
            <li>→ 저가 ~ VIP 다양한 지출 배경</li>
          </ul>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class="mth">
          <div class="mth-ttl">Data Collection</div>
          <ul>
            <li>→ Google Forms 온라인 설문</li>
            <li>→ 익명 자가 보고 방식</li>
            <li>→ 학생 네트워크 배포</li>
            <li>→ 자발적 참여, 인센티브 없음</li>
          </ul>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown("""<div class="mth">
          <div class="mth-ttl">Analysis Method</div>
          <ul>
            <li>→ 연령대별 티켓 선호 패턴 비교</li>
            <li>→ 지출 수준별 만족도 분석</li>
            <li>→ 좌석 유형 × 만족도 교차분석</li>
            <li>→ 주요 구매 동기 요인 식별</li>
          </ul>
        </div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
#  06 — SURVEY QUESTIONS
# ══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<p class="lbl">06 — Survey Questions</p>', unsafe_allow_html=True)
    st.markdown('<p class="ttl">The <em>7 questions</em></p>', unsafe_allow_html=True)
 
    survey_qs = [
        ("Q1","연령대가 어떻게 되세요?",
         ["10대 (Under 20)","20대 (20–29)","30대 이상 (30+)"]),
        ("Q2","콘서트에 얼마나 자주 가세요?",
         ["자주 간다 (Often)","가끔 간다 (Sometimes)","거의 안 간다 (Rarely)"]),
        ("Q3","티켓 구매 시 가장 중요한 요소는?",
         ["가격 (Price)","좌석 위치 (Seat)","아티스트 (Artist)","공연장 (Venue)","굿즈/혜택 (Merch)"]),
        ("Q4","보통 콘서트 티켓에 얼마를 쓰세요?",
         ["$50 미만","$50–$100","$100 이상"]),
        ("Q5","선호하는 좌석 구역은?",
         ["VIP","중간 좌석 (Middle)","저가 좌석 (Budget)"]),
        ("Q6","콘서트 경험에 얼마나 만족하세요? (1–5)",
         ["1 — 매우 불만족","2 — 불만족","3 — 보통","4 — 만족","5 — 매우 만족"]),
        ("Q7","좋아하는 아티스트라면 비싼 티켓도 사겠어요?",
         ["Yes — 무조건 산다","No — 가격이 중요하다"]),
    ]
    for qn, qt, opts in survey_qs:
        pills = "".join(f'<span class="pill">{o}</span>' for o in opts)
        st.markdown(f"""
        <div class="sq">
          <div class="sq-n">{qn}</div>
          <p class="sq-txt">{qt}</p>
          <div>{pills}</div>
        </div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
#  07 — DATA
# ══════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<p class="lbl">07 — Example Data</p>', unsafe_allow_html=True)
    st.markdown('<p class="ttl">Sample <em>results</em></p>', unsafe_allow_html=True)
    st.caption("데이터 구성 근거: 문화체육관광부·예술경영지원센터 '2025년 공연시장 티켓판매 현황 분석 보고서'")
 
    avg_sat   = round(DF["sat"].mean(), 1)
    avg_spend = int(DF["spend"].mean())
    vip_pct   = round(len(DF[DF["seat"]=="VIP"]) / len(DF) * 100)
    s1,s2,s3,s4 = st.columns(4)
    with s1: st.metric("👥 총 참여자",   "20명")
    with s2: st.metric("⭐ 평균 만족도", f"{avg_sat} / 5")
    with s3: st.metric("💰 평균 지출",   f"${avg_spend}")
    with s4: st.metric("💎 VIP 비율",    f"{vip_pct}%")
 
    st.divider()
 
    ch1, ch2 = st.columns(2, gap="medium")
    with ch1:
        st.markdown("**🪑 좌석 선호도**")
        st.plotly_chart(ch_donut(DF), use_container_width=True, key="d1")
    with ch2:
        st.markdown("**📈 지출 vs 만족도**")
        st.plotly_chart(ch_scatter(DF), use_container_width=True, key="d2")
 
    ch3, ch4 = st.columns(2, gap="medium")
    with ch3:
        st.markdown("**💸 연령대별 평균 지출**")
        st.plotly_chart(ch_spend(DF), use_container_width=True, key="d3")
    with ch4:
        st.markdown("**🏆 좌석별 평균 만족도**")
        st.plotly_chart(ch_seat_sat(DF), use_container_width=True, key="d4")
 
    st.markdown("**📅 관람 빈도 분포**")
    st.plotly_chart(ch_freq(DF), use_container_width=True, key="d5")
 
    st.divider()
    st.markdown("**🔍 데이터 패턴**")
    i1, i2 = st.columns(2, gap="medium")
    with i1:
        st.markdown("""
        <div class="ins"><p class="ins-lbl">Pattern 01 — 팬덤 충성층</p>
          <p>20대 VIP(P01–P05) 모두 만족도 <strong>5/5</strong>, 평균 지출 $157. 대중음악 매출 29% 성장을 이끈 팬덤 소비 구조와 정확히 일치.</p></div>
        <div class="ins"><p class="ins-lbl">Pattern 02 — 10대 경제적 제약</p>
          <p>10대(P09–P12) 평균 지출 $34, 평균 만족도 2.5. 관람률 60.2% 중 신규 유입이 미미한 이유를 설명하는 그룹.</p></div>
        """, unsafe_allow_html=True)
    with i2:
        st.markdown("""
        <div class="ins"><p class="ins-lbl">Pattern 03 — 30대+ 가성비</p>
          <p>30대+(P13–P16) 중간 좌석 평균 $89, 만족도 4.0. 관광 연계 소비(이동 시 지출 +30%) 반영한 최고 가성비 그룹.</p></div>
        <div class="ins"><p class="ins-lbl">Pattern 04 — 관람률 역설</p>
          <p>P17·P18처럼 거의 안 가는 그룹도 존재. 시장 매출은 크게 늘었지만 관람률 -2.8%p — 소수가 자주, 많이 쓰는 구조.</p></div>
        """, unsafe_allow_html=True)
 
    st.divider()
    with st.expander("📋 전체 20명 데이터 보기"):
        d = DF.copy()
        d.columns = ["참여자","연령대","빈도","좌석","지출($)","만족도"]
        st.dataframe(
            d.style.background_gradient(subset=["만족도"],cmap="YlOrRd")
                   .background_gradient(subset=["지출($)"],cmap="Blues"),
            use_container_width=True, hide_index=True)
 
# ══════════════════════════════════════════════════════════════
#  08 — EXPECTED RESULTS
# ══════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<p class="lbl">08 — Expected Results</p>', unsafe_allow_html=True)
    st.markdown('<p class="ttl">What we <em>predict</em></p>', unsafe_allow_html=True)
 
    hyps = [
        ("Hypothesis A","연령대 & 지출 패턴",
         "10대는 경제적 제약으로 $50 미만에 집중, 20대는 VIP·프리미엄 좌석 지출 의향이 높을 것. 특히 좋아하는 아티스트 공연일 때 더욱 두드러진다."),
        ("Hypothesis B","좌석 vs 만족도",
         "VIP 보유자가 더 높은 만족도(4–5)를 보고할 것으로 예측. 단, 저가 좌석 관객도 군중 에너지와 감성적 연결로 지출 수준보다 높은 만족도를 기록할 수 있다."),
        ("Hypothesis C","아티스트 = 최우선 구매 동기",
         "아티스트 인기가 가격·좌석보다 강한 구매 동인 — 2025년 대중음악 매출 29% 성장을 이끈 팬덤 충성도 연구와 일치한다."),
        ("Hypothesis D","기대치 효과",
         "만족도는 단순 지출액보다 공연이 사전 기대에 부응했는지와 더 강하게 상관될 것. Pine & Gilmore 경험 경제 모델과 일치: the framing shapes the feeling."),
    ]
    col1, col2 = st.columns(2, gap="medium")
    for i,(icon,title,body) in enumerate(hyps):
        with (col1 if i%2==0 else col2):
            st.markdown(f"""
            <div class="exc">
              <div class="exc-icon">{icon}</div>
              <h3>{title}</h3>
              <p>{body}</p>
            </div>""", unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════
#  09 — CONCLUSION
# ══════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<p class="lbl">09 — Conclusion</p>', unsafe_allow_html=True)
 
    col_l, col_r = st.columns([1, 1.5], gap="large")
    with col_l:
        st.markdown("""
        <div class="conc-big">
          THE<br><span class="r">TICKET</span><br>
          IS<br><span class="a">NOT</span><br>
          JUST<br>A TICKET
        </div>""", unsafe_allow_html=True)
    with col_r:
        st.markdown("""
        <div class="conc-body">
          <p>콘서트 티켓 구매는 단순한 경제적 결정이 아닙니다. 그것은 <strong>사회적, 감정적, 문화적 행위</strong>입니다. 어떤 티켓을 살지, 얼마를 낼지의 선택은 공연장 문이 열리기 훨씬 전부터 경험을 형성합니다.</p>
          <p>공연 기획자들은 이 데이터를 활용해 <strong>더 나은 가격 구조</strong>를 설계하고, 각 좌석 등급의 인지 가치를 높이며, 프리미엄 지출을 정당화하는 경험을 만들 수 있습니다.</p>
          <p>신진 아티스트에게는 <strong>합리적 가격 + 강한 무대 존재감</strong>이 화려한 프로덕션보다 달러당 더 높은 만족도를 제공한다는 것을 발견할 수도 있습니다.</p>
          <p>공연학적 관점에서: 관객은 공연의 수동적 수용자가 아닙니다. 그들은 <strong>경험의 능동적 공동 창조자</strong>입니다.</p>
          <div class="conc-credit">
            Research by <em>Yeryung Go</em> · Korea Dance · SKKU · 2025<br>
            데이터 출처: 문화체육관광부·예술경영지원센터 2025 공연시장 보고서
          </div>
        </div>""", unsafe_allow_html=True)
 
    st.divider()
    st.markdown("**📊 핵심 데이터 요약**")
    fc1, fc2, fc3 = st.columns(3, gap="medium")
    with fc1:
        st.markdown("좌석 선호도")
        st.plotly_chart(ch_donut(DF), use_container_width=True, key="c1")
    with fc2:
        st.markdown("좌석별 평균 만족도")
        st.plotly_chart(ch_seat_sat(DF), use_container_width=True, key="c2")
    with fc3:
        st.markdown("만족도 전체 분포")
        st.plotly_chart(ch_hist(DF), use_container_width=True, key="c3")
 
