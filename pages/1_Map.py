"""지도 - 한옥 다방 Aesthetic"""

import streamlit as st
import folium
from streamlit_folium import st_folium

from utils.data_loader import get_venues_df, get_accommodation, CATEGORY_INFO

st.set_page_config(
    page_title="지도 - 담양 리트릿",
    page_icon="🎋",
    layout="centered",
)

# Same design system
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600&display=swap');

:root {
    --hanji: #FDF8F3;
    --wood: #5D4037;
    --bamboo: #4A6741;
    --bamboo-light: #7A9E7E;
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
    color: var(--ink);
}

.base-banner strong {
    color: var(--bamboo);
}

.filter-section {
    background: white;
    border-radius: 12px;
    padding: 0.75rem;
    margin-bottom: 0.75rem;
    border: 1px solid rgba(93, 64, 55, 0.1);
}

.stButton > button {
    background: var(--wood) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
}

.stCheckbox label {
    font-size: 0.9rem !important;
}

.legend-bar {
    display: flex;
    justify-content: space-around;
    background: white;
    border-radius: 10px;
    padding: 0.5rem;
    margin-top: 0.75rem;
    font-size: 0.75rem;
    border: 1px solid rgba(93, 64, 55, 0.1);
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("← 홈으로", type="secondary"):
    st.switch_page("app.py")

st.markdown('<h1 class="page-title">🗺️ 담양 지도</h1>', unsafe_allow_html=True)

# Load data
df = get_venues_df()
accommodation = get_accommodation()

# Base banner
st.markdown("""
<div class="base-banner">
    <strong>🏡 BASE</strong> 담양힐링파크 새연리조트 (봉산면) · 🔴 빨간 마커
</div>
""", unsafe_allow_html=True)

# Category filter
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    show_restaurant = st.checkbox("🍚 식당", value=True)
with col2:
    show_cafe = st.checkbox("☕ 카페", value=True)
with col3:
    show_activity = st.checkbox("🎨 Activity", value=True)
st.markdown('</div>', unsafe_allow_html=True)

# Filter data
categories = []
if show_restaurant: categories.append("restaurant")
if show_cafe: categories.append("cafe")
if show_activity: categories.append("activity")

filtered_df = df[df["category"].isin(categories)] if categories else df
st.caption(f"{len(filtered_df)}개 장소 표시")

# Create map with warm tones
m = folium.Map(
    location=[accommodation["lat"], accommodation["lng"]],
    zoom_start=11,
    tiles="cartodbpositron",
)

# Distance circles with warm colors
folium.Circle(
    location=[accommodation["lat"], accommodation["lng"]],
    radius=5000,
    color="#5D4037",
    weight=2,
    fill=True,
    fill_opacity=0.05,
    popup="5km",
).add_to(m)

folium.Circle(
    location=[accommodation["lat"], accommodation["lng"]],
    radius=10000,
    color="#C17F59",
    weight=1,
    fill=False,
    popup="10km",
).add_to(m)

# Accommodation marker with emphasis
folium.CircleMarker(
    location=[accommodation["lat"], accommodation["lng"]],
    radius=18,
    color="#dc2626",
    weight=3,
    fill=True,
    fill_color="#fecaca",
    fill_opacity=0.6,
).add_to(m)

folium.Marker(
    location=[accommodation["lat"], accommodation["lng"]],
    popup=folium.Popup(
        f"""<div style="text-align:center; min-width:120px; font-family: sans-serif;">
            <b style="color:#dc2626;">🏡 BASE</b><br>
            {accommodation['name'][:10]}...
        </div>""",
        max_width=150
    ),
    icon=folium.Icon(color="red", icon="home", prefix="fa"),
).add_to(m)

# Venue markers
color_map = {"restaurant": "green", "cafe": "orange", "activity": "purple"}
icon_map = {"restaurant": "utensils", "cafe": "coffee", "activity": "palette"}

for _, row in filtered_df.iterrows():
    cat = row["category"]
    popup_text = f"<b>{row['name']}</b><br><small>{row['feature']}</small>"

    folium.Marker(
        location=[row["lat"], row["lng"]],
        popup=folium.Popup(popup_text, max_width=180),
        tooltip=row["name"],
        icon=folium.Icon(color=color_map.get(cat, "gray"), icon=icon_map.get(cat, "info"), prefix="fa"),
    ).add_to(m)

# Render map
st_folium(m, width=None, height=420, use_container_width=True)

# Legend
st.markdown("""
<div class="legend-bar">
    <span class="legend-item">🔴 숙소</span>
    <span class="legend-item">🟢 식당</span>
    <span class="legend-item">🟠 카페</span>
    <span class="legend-item">🟣 샵</span>
</div>
""", unsafe_allow_html=True)

# Venue list
st.markdown("---")
for cat in categories:
    cat_df = filtered_df[filtered_df["category"] == cat]
    if not cat_df.empty:
        emoji = CATEGORY_INFO[cat]["emoji"]
        label = CATEGORY_INFO[cat]["label"]
        with st.expander(f"{emoji} {label} ({len(cat_df)})", expanded=False):
            for _, row in cat_df.iterrows():
                url_link = f" [→]({row['url']})" if row['url'] else ""
                st.markdown(f"**{row['name']}** - {row['feature']}{url_link}")
