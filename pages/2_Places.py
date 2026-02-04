"""장소 목록 - 한옥 다방 Aesthetic"""

import streamlit as st
from utils.data_loader import get_venues_df, get_accommodation, calculate_distance, CATEGORY_INFO

st.set_page_config(
    page_title="목록 - 담양 리트릿",
    page_icon="🎋",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600&display=swap');

:root {
    --hanji: #FDF8F3;
    --wood: #5D4037;
    --bamboo: #4A6741;
    --sienna: #C17F59;
    --cream: #F5EDE4;
    --ink: #2C2416;
    --ink-light: #6B5D4D;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background: var(--hanji) !important;
}

.stApp {
    background: linear-gradient(180deg, var(--hanji) 0%, var(--cream) 100%);
}

.block-container { padding: 1rem 1rem !important; }
#MainMenu, footer, header {visibility: hidden;}

.page-title {
    font-family: 'Gowun Batang', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--wood);
    margin: 0.5rem 0;
}

.base-banner {
    background: linear-gradient(135deg, #FFF9F0 0%, #FDF3E7 100%);
    border: 1px solid var(--sienna);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.85rem;
}

.venue-card {
    background: white;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.6rem;
    border: 1px solid rgba(93, 64, 55, 0.08);
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.venue-card:hover {
    border-color: var(--sienna);
}

.venue-name {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--ink);
}

.venue-detail {
    font-size: 0.8rem;
    color: var(--ink-light);
    margin-top: 0.2rem;
}

.venue-meta {
    font-size: 0.7rem;
    color: var(--bamboo);
    margin-top: 0.3rem;
}

.category-badge {
    display: inline-block;
    font-size: 0.65rem;
    padding: 0.15rem 0.5rem;
    border-radius: 6px;
    margin-bottom: 0.4rem;
}

.cat-restaurant { background: rgba(74, 103, 65, 0.15); color: var(--bamboo); }
.cat-cafe { background: rgba(193, 127, 89, 0.15); color: var(--sienna); }
.cat-activity { background: rgba(93, 64, 55, 0.15); color: var(--wood); }

.stButton > button {
    background: var(--wood) !important;
    color: white !important;
    border-radius: 12px !important;
}

.stLinkButton > a {
    background: var(--cream) !important;
    color: var(--wood) !important;
    border: 1px solid var(--sienna) !important;
    border-radius: 10px !important;
}

.stTextInput input {
    border-radius: 12px !important;
    border-color: var(--sienna) !important;
}
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("← 홈으로", type="secondary"):
    st.switch_page("app.py")

st.markdown('<h1 class="page-title">📋 장소 목록</h1>', unsafe_allow_html=True)

# Load data
df = get_venues_df()
accommodation = get_accommodation()

# Calculate distances
df["distance_km"] = df.apply(
    lambda row: calculate_distance(accommodation["lat"], accommodation["lng"], row["lat"], row["lng"]),
    axis=1
)

# Base banner
st.markdown("""
<div class="base-banner">
    <strong style="color: #4A6741;">🏡 BASE</strong> 담양힐링파크 새연리조트 · 거리순 정렬
</div>
""", unsafe_allow_html=True)

# Search
search = st.text_input("🔍 검색", placeholder="장소명, 특징...")

# Category filter
col1, col2, col3 = st.columns(3)
with col1:
    show_restaurant = st.checkbox("🍚 식당", value=True, key="r")
with col2:
    show_cafe = st.checkbox("☕ 카페", value=True, key="c")
with col3:
    show_activity = st.checkbox("🎨 Activity", value=True, key="a")

# Apply filters
categories = []
if show_restaurant: categories.append("restaurant")
if show_cafe: categories.append("cafe")
if show_activity: categories.append("activity")

filtered = df[df["category"].isin(categories)] if categories else df

if search:
    search_lower = search.lower()
    filtered = filtered[
        filtered["name"].str.lower().str.contains(search_lower, na=False) |
        filtered["feature"].str.lower().str.contains(search_lower, na=False)
    ]

filtered = filtered.sort_values("distance_km")
st.caption(f"{len(filtered)}개 장소")
st.markdown("---")

# Display venues
cat_colors = {"restaurant": "cat-restaurant", "cafe": "cat-cafe", "activity": "cat-activity"}

for _, row in filtered.iterrows():
    cat = row["category"]
    cat_info = CATEGORY_INFO.get(cat, {"emoji": "", "label": cat})
    badge_class = cat_colors.get(cat, "cat-cafe")

    hours_text = f"🕐 {row['hours']}" if row.get('hours') else ""
    note_text = f"💡 {row['note']}" if row.get('note') else ""
    meta_parts = [p for p in [hours_text, f"📍 {row['distance_km']:.1f}km", note_text] if p]

    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
        <div class="venue-card">
            <span class="category-badge {badge_class}">{cat_info['emoji']} {cat_info['label']}</span>
            <div class="venue-name">{row['name']}</div>
            <div class="venue-detail">{row['feature']}</div>
            <div class="venue-meta">{' · '.join(meta_parts)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if row['url']:
            st.link_button("🔗", row['url'], use_container_width=True)

# CSV Download
st.markdown("---")
if st.button("📥 CSV 다운로드"):
    csv_df = filtered[["name", "category", "feature", "address", "hours", "distance_km"]]
    csv_df.columns = ["장소명", "카테고리", "특징", "주소", "운영시간", "거리(km)"]
    csv = csv_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("다운로드", csv, "damyang_venues.csv", "text/csv")
