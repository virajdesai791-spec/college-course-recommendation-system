import streamlit as st
import pandas as pd
import html
import matplotlib.pyplot as plt

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Smart College Course Recommendation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# FUTURISTIC DARK THEME
# =========================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #241044 0%, transparent 35%),
        radial-gradient(ellipse at 90% 10%, #08294b 0%, transparent 35%),
        linear-gradient(135deg, #070912 0%, #0b1020 55%, #10091d 100%);
    color: #e9e4ff !important;
}

html, body, [class*="css"] {
    color: #e9e4ff !important;
}

[data-testid="stHeader"] {
    background: rgba(7, 9, 18, 0.75) !important;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #0b0d1b 0%, #0d1020 50%, #120b20 100%) !important;
    border-right: 1px solid rgba(167, 139, 250, 0.22) !important;
}

[data-testid="stSidebar"] * {
    color: #ddd6fe !important;
}

/* =========================================================
   HEADINGS / TEXT
   ========================================================= */

h1, h2, h3, h4, h5, h6 {
    color: #f5f3ff !important;
}

p, li, label, span {
    color: #ddd6fe;
}

.stCaption, [data-testid="stCaptionContainer"] {
    color: #9f9bb5 !important;
}

/* =========================================================
   HERO
   ========================================================= */

.hero {
    padding: 34px 38px;
    border-radius: 26px;
    margin-bottom: 28px;
    background:
        radial-gradient(circle at 15% 20%, rgba(124,58,237,0.25), transparent 32%),
        radial-gradient(circle at 85% 15%, rgba(14,165,233,0.18), transparent 30%),
        linear-gradient(135deg, rgba(15,18,35,0.96), rgba(19,12,35,0.94));
    border: 1px solid rgba(167,139,250,0.35);
    box-shadow:
        0 0 35px rgba(124,58,237,0.12),
        inset 0 0 30px rgba(59,130,246,0.04);
}

.hero-kicker {
    color: #a78bfa !important;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 12px;
}

.hero-title {
    font-size: clamp(32px, 4vw, 52px);
    line-height: 1.12;
    margin: 0 0 15px 0;
    color: #f5f3ff !important;
    font-weight: 800;
}

.hero-title span {
    color: #a78bfa !important;
}

.hero-description {
    color: #b9b4ca !important;
    font-size: 16px;
    line-height: 1.7;
    max-width: 900px;
}

.hero-chip {
    display: inline-block;
    padding: 7px 12px;
    margin: 8px 7px 0 0;
    border-radius: 999px;
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(167,139,250,0.25);
    color: #c4b5fd !important;
    font-size: 12px;
    font-weight: 700;
}

.hero-credit {
    text-align: right;
    color: #c4b5fd !important;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin-top: 12px;
}

/* =========================================================
   SECTION CARDS
   ========================================================= */

.glass-card {
    background: rgba(15, 18, 35, 0.82);
    border: 1px solid rgba(167,139,250,0.20);
    border-radius: 20px;
    padding: 22px;
    margin: 10px 0 18px 0;
    box-shadow: 0 12px 35px rgba(0,0,0,0.20);
}

.feature-card {
    background: linear-gradient(145deg, rgba(17,19,34,0.95), rgba(25,17,46,0.92));
    border: 1px solid rgba(167,139,250,0.22);
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.18);
}

.feature-title {
    color: #c4b5fd !important;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 8px;
}

.feature-text {
    color: #a9a4b8 !important;
    font-size: 13px;
    line-height: 1.55;
}

/* =========================================================
   SIDEBAR SELECTBOXES - NO WHITE
   ========================================================= */

section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #111322 !important;
    border: 1px solid rgba(167,139,250,0.38) !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #c4b5fd !important;
    -webkit-text-fill-color: #c4b5fd !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] input {
    color: #c4b5fd !important;
    -webkit-text-fill-color: #c4b5fd !important;
}

section[data-testid="stSidebar"] div[data-testid="stSelectbox"] svg {
    fill: #a78bfa !important;
    color: #a78bfa !important;
}

section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"]:hover > div {
    border-color: #8b5cf6 !important;
    background: #15172a !important;
}

/* Dropdown popup */
div[data-baseweb="popover"],
div[role="listbox"] {
    background: #111322 !important;
    border: 1px solid rgba(167,139,250,0.35) !important;
    box-shadow: 0 15px 45px rgba(0,0,0,0.50) !important;
}

div[role="listbox"] div[role="option"] {
    background: #111322 !important;
    color: #c4b5fd !important;
    -webkit-text-fill-color: #c4b5fd !important;
}

div[role="listbox"] div[role="option"]:hover {
    background: #27204a !important;
    color: #e9ddff !important;
    -webkit-text-fill-color: #e9ddff !important;
}

div[role="listbox"] div[role="option"][aria-selected="true"] {
    background: #31205f !important;
    color: #d8ccff !important;
    -webkit-text-fill-color: #d8ccff !important;
    font-weight: 700 !important;
}

/* =========================================================
   SIDEBAR INPUTS / SLIDER
   ========================================================= */

section[data-testid="stSidebar"] input {
    background: #111322 !important;
    color: #ddd6fe !important;
    -webkit-text-fill-color: #ddd6fe !important;
    border-color: rgba(167,139,250,0.35) !important;
}

section[data-testid="stSidebar"] [data-testid="stSlider"] {
    padding-top: 5px;
}

section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: #a78bfa !important;
}

/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    background: linear-gradient(135deg, #6d28d9, #2563eb) !important;
    color: #ffffff !important;
    border: 1px solid rgba(196,181,253,0.35) !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    min-height: 44px;
    box-shadow: 0 8px 25px rgba(76,29,149,0.25);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    color: #ffffff !important;
    border-color: #a78bfa !important;
    transform: translateY(-1px);
}

/* =========================================================
   TEXT INPUTS / SEARCH
   ========================================================= */

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: #111322 !important;
    color: #e9ddff !important;
    -webkit-text-fill-color: #e9ddff !important;
    border: 1px solid rgba(167,139,250,0.35) !important;
    border-radius: 12px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #77738a !important;
    -webkit-text-fill-color: #77738a !important;
}

/* =========================================================
   METRICS
   ========================================================= */

[data-testid="stMetric"] {
    background: rgba(17,19,34,0.86) !important;
    border: 1px solid rgba(167,139,250,0.20) !important;
    border-radius: 16px !important;
    padding: 14px !important;
}

[data-testid="stMetricLabel"] {
    color: #9f9bb5 !important;
}

[data-testid="stMetricValue"] {
    color: #c4b5fd !important;
}

/* =========================================================
   TABS
   ========================================================= */

button[data-baseweb="tab"] {
    color: #aaa5ba !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #c4b5fd !important;
}

div[data-baseweb="tab-highlight"] {
    background-color: #8b5cf6 !important;
}

/* =========================================================
   EXPANDERS
   ========================================================= */

div[data-testid="stExpander"] {
    background: rgba(17,19,34,0.72) !important;
    border: 1px solid rgba(167,139,250,0.20) !important;
    border-radius: 15px !important;
}

div[data-testid="stExpander"] summary {
    color: #ddd6fe !important;
}

/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    background: #111322 !important;
    color: #ddd6fe !important;
    border-color: rgba(167,139,250,0.25) !important;
}

/* =========================================================
   CUSTOM COLLEGE RESULTS TABLE
   ========================================================= */

.college-table-wrap {
    max-height: 650px;
    overflow: auto;
    border: 1px solid rgba(167,139,250,0.24);
    border-radius: 16px;
    background: #0e1020;
}

.college-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    color: #c4b5fd;
}

.college-table th {
    position: sticky;
    top: 0;
    z-index: 2;
    background: #17132b !important;
    color: #d8ccff !important;
    text-align: left;
    padding: 13px 12px;
    border-bottom: 1px solid rgba(167,139,250,0.28);
    font-weight: 800;
}

.college-table td {
    background: #0e1020 !important;
    color: #c4b5fd !important;
    padding: 11px 12px;
    border-bottom: 1px solid rgba(167,139,250,0.10);
    vertical-align: top;
}

.college-table tr:hover td {
    background: #17142b !important;
    color: #e5dcff !important;
}

.score-badge {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    background: #31205f;
    color: #d8ccff !important;
    font-weight: 800;
}

/* =========================================================
   DATAFRAME FALLBACK
   ========================================================= */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(167,139,250,0.22) !important;
    border-radius: 14px !important;
}

/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    margin-top: 35px;
    padding: 22px;
    text-align: center;
    border-top: 1px solid rgba(167,139,250,0.18);
    color: #77738a !important;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA LOADING
# =========================================================

@st.cache_data
def load_main_data():
    df = pd.read_csv("college_courses_combined.csv")
    object_columns = df.select_dtypes(include="object").columns
    for column in object_columns:
        df[column] = df[column].fillna("").astype(str).str.strip()
    return df


@st.cache_data
def load_quality_data():
    try:
        quality = pd.read_csv("college_quality_data.csv")
        object_columns = quality.select_dtypes(include="object").columns
        for column in object_columns:
            quality[column] = quality[column].fillna("").astype(str).str.strip()
        return quality
    except Exception:
        return pd.DataFrame()


df = load_main_data()
quality_df = load_quality_data()

# =========================================================
# SESSION STATE
# =========================================================

if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

# =========================================================
# HERO
# =========================================================


st.markdown("""
<div style="
background:#111827;
border:1px solid #8b5cf6;
border-radius:25px;
padding:40px;
margin:10px 0 28px 0;
">

<h1 style="
color:#c4b5fd;
font-size:42px;
margin-bottom:15px;
">
🎓 Smart College Course Recommendation System
</h1>

<p style="
color:#e5e7eb;
font-size:18px;
">
Find the right college and course using real college data.
</p>

<div style="
text-align:right;
margin-top:30px;
color:#c4b5fd;
font-weight:bold;
letter-spacing:2px;
">
DESIGNED &amp; DEVELOPED BY<br>
<span style="font-size:24px;">
VIRAJ DESAI
</span>
</div>

</div>
""", unsafe_allow_html=True)
# =========================================================
# PLATFORM OVERVIEW
# =========================================================

st.markdown("## 🚀 Explore the Platform")

feature_cols = st.columns(3)

features = [
    (
        "🔎 Course Discovery",
        "Filter programmes, disciplines, states, districts and study modes to find suitable courses."
    ),
    (
        "⚖️ College Comparison",
        "Compare colleges using course availability, location, recommendation score and quality information."
    ),
    (
        "📊 Quality Insights",
        "View available NAAC accreditation and CGPA information for colleges where verified data is available."
    ),
]

for col, (title, description) in zip(feature_cols, features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-title">{title}</div>
                <div class="feature-text">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("## 🎯 Find Your Course")
st.sidebar.caption("Choose your preferences and discover matching colleges.")

programmes = ["All Programmes"] + sorted(
    df["Programme"].dropna().unique().tolist()
)

selected_programme = st.sidebar.selectbox(
    "📘 Programme",
    programmes
)

# Discipline depends on selected Programme
# Discipline depends on selected Programme
if selected_programme == "All Programmes":
    discipline_df = df
else:
    discipline_df = df[df["Programme"] == selected_programme]

disciplines = ["All Disciplines"] + sorted(
    discipline_df["Discipline"].dropna().unique().tolist()
)

states = ["All States"] + sorted(
    df["State Name"].dropna().unique().tolist()
)

modes = ["All Modes"] + sorted(
    df["Mode"].dropna().unique().tolist()
)

selected_discipline = st.sidebar.selectbox(
    "🧠 Discipline",
    disciplines
)

selected_state = st.sidebar.selectbox(
    "📍 State",
    states
)
# Districts depend on selected State
if selected_state == "All States":
    district_options = sorted(
        df["District Name"].dropna().unique().tolist()
    )
else:
    district_options = sorted(
        df.loc[
            df["State Name"] == selected_state,
            "District Name"
        ].dropna().unique().tolist()
    )

districts = ["All Districts"] + district_options

selected_district = st.sidebar.selectbox(
    "🏙️ District",
    districts
)

selected_mode = st.sidebar.selectbox(
    "💻 Mode",
    modes
)

marks = st.sidebar.slider(
    "📝 Your Marks (%)",
    min_value=0,
    max_value=100,
    value=75,
    step=1
)

find_colleges = st.sidebar.button(
    "🔍 Find My Colleges",
    use_container_width=True
)

if find_colleges:
    st.session_state.search_clicked = True

# =========================================================
# FILTER DATA
# =========================================================

results = df.copy()

if selected_programme != "All Programmes":
    results = results[results["Programme"] == selected_programme]

if selected_discipline != "All Disciplines":
    results = results[results["Discipline"] == selected_discipline]

if selected_state != "All States":
    results = results[results["State Name"] == selected_state]

if selected_district != "All Districts":
    results = results[results["District Name"] == selected_district]

if selected_mode != "All Modes":
    results = results[results["Mode"] == selected_mode]



# =========================================================
# FEATURE ENGINEERING - RECOMMENDATION MATCH SCORE
# =========================================================

# Create a new Match Score feature using existing course preferences.
score = pd.Series(0.0, index=results.index)

if selected_programme != "All Programmes":
    score += (results["Programme"] == selected_programme).astype(float) * 30

if selected_discipline != "All Disciplines":
    score += (results["Discipline"] == selected_discipline).astype(float) * 30

if selected_state != "All States":
    score += (results["State Name"] == selected_state).astype(float) * 20

if selected_district != "All Districts":
    score += (results["District Name"] == selected_district).astype(float) * 10

if selected_mode != "All Modes":
    score += (results["Mode"] == selected_mode).astype(float) * 10

# Marks influence the recommendation slightly.
marks_bonus = min(max(marks, 0), 100) / 100 * 5
score += marks_bonus

results["Match Score"] = score.clip(upper=100).round(1)

# Remove duplicate college-course combinations where possible for display.
display_results = results.drop_duplicates(
    subset=["InstituteName", "State Name", "District Name"],
    keep="first"
).copy()

display_results = display_results.sort_values(
    by=["Match Score", "InstituteName"],
    ascending=[False, True]
)

# =========================================================
# COLLEGE SEARCH
# =========================================================

st.markdown("## 🏫 College Results")

search_text = st.text_input(
    "🏫 Search College Name",
    placeholder="Type a college name, then press Enter...",
    key="college_search"
)

if search_text.strip():
    search_lower = search_text.strip().lower()

    display_results = display_results[
        display_results["InstituteName"]
        .str.lower()
        .str.contains(
            search_lower,
            na=False,
            regex=False
        )
    ]
# =========================================================
# RESULT METRICS
# =========================================================

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric("🎓 Matching Records", f"{len(results):,}")

with metric2:
    st.metric(
        "🏫 Colleges Found",
        f"{display_results['InstituteName'].nunique():,}"
    )

with metric3:
    st.metric("🗺️ States", f"{display_results['State Name'].nunique():,}")

with metric4:
    best_score = float(display_results["Match Score"].max()) if not display_results.empty else 0
    st.metric("⭐ Best Match", f"{best_score:.1f}%")

# =========================================================
# CUSTOM COLLEGE RESULTS TABLE
# =========================================================

if display_results.empty:
    st.warning("No colleges found for the selected filters. Try changing your preferences.")
else:
    visible_columns = [
        "InstituteName",
        "State Name",
        "District Name",
        "Programme",
        "Discipline",
        "Mode",
        "Match Score"
    ]

    table_results = display_results.loc[
        :,
        [column for column in visible_columns if column in display_results.columns]
    ].head(100).copy()

    rows_html = []

    for _, college_row in table_results.iterrows():
        cells = []

        for column in table_results.columns:
            value = college_row[column]

            if column == "Match Score":
                cell = f'<td><span class="score-badge">{float(value):.1f}%</span></td>'
            else:
                cell = f'<td>{html.escape(str(value))}</td>'

            cells.append(cell)

        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    headers_html = "".join(
        f"<th>{html.escape(column)}</th>"
        for column in table_results.columns
    )

    table_html = f"""
    <div class="college-table-wrap">
        <table class="college-table">
            <thead>
                <tr>{headers_html}</tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    </div>
    """

    st.markdown(table_html, unsafe_allow_html=True)
    st.caption(f"Showing up to 100 matching colleges. Total matching records: {len(results):,}")

    # =====================================================
    # CSV DOWNLOAD
    # =====================================================

    csv_data = display_results.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Results as CSV",
        data=csv_data,
        file_name="college_recommendations.csv",
        mime="text/csv",
        use_container_width=True
    )

# =========================================================
# PREFERENCE SUMMARY
# =========================================================

st.markdown("## 🧾 Preference Summary")

summary_cols = st.columns(5)

summary_values = [
    ("Programme", selected_programme),
    ("Discipline", selected_discipline),
    ("State", selected_state),
    ("District", selected_district),
    ("Mode", selected_mode),
]

for col, (label, value) in zip(summary_cols, summary_values):
    with col:
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="color:#8f8aa0;font-size:12px;">{html.escape(label)}</div>
                <div style="color:#c4b5fd;font-weight:700;font-size:14px;margin-top:5px;">
                    {html.escape(str(value))}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# COLLEGE PROFILE
# =========================================================

st.markdown("## 🏫 College Profile")

profile_options = ["Select a college"]

if not display_results.empty:
    profile_options += display_results["InstituteName"].drop_duplicates().head(100).tolist()

selected_college = st.selectbox(
    "Select a college to view its profile",
    profile_options,
    key="profile_college"
)

if selected_college != "Select a college":
    college_rows = df[df["InstituteName"] == selected_college].copy()

    if not college_rows.empty:
        first_row = college_rows.iloc[0]

        profile_col1, profile_col2 = st.columns(2)

        with profile_col1:
            st.markdown(
                f"""
                <div class="glass-card">
                    <h3>🎓 {html.escape(selected_college)}</h3>
                    <p><b>State:</b> {html.escape(str(first_row["State Name"]))}</p>
                    <p><b>District:</b> {html.escape(str(first_row["District Name"]))}</p>
                    <p><b>Level:</b> {html.escape(str(first_row["Level"]))}</p>
                    <p><b>Total Course Records:</b> {len(college_rows):,}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with profile_col2:
            profile_programmes = ", ".join(
                sorted(college_rows["Programme"].dropna().unique().tolist())
            )
            profile_disciplines = ", ".join(
                sorted(college_rows["Discipline"].dropna().unique().tolist())
            )

            st.markdown(
                f"""
                <div class="glass-card">
                    <h3>📚 Available Courses</h3>
                    <p><b>Programmes:</b> {html.escape(profile_programmes)}</p>
                    <p><b>Disciplines:</b> {html.escape(profile_disciplines)}</p>
                    <p><b>Modes:</b> {html.escape(", ".join(sorted(college_rows["Mode"].unique())))}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================================================
# QUALITY & ACCREDITATION
# =========================================================

st.markdown("## 🏆 Quality & Accreditation")

quality_view = pd.DataFrame()

if not quality_df.empty and selected_college != "Select a college":
    quality_view = quality_df[
        quality_df["InstituteName"].str.lower() == selected_college.lower()
    ].copy()

if selected_college == "Select a college":
    st.info("Select a college above to view available quality and accreditation information.")
elif quality_view.empty:
    st.info("Verified quality/accreditation data is not available for this college in the current quality dataset.")
else:
    qrow = quality_view.iloc[0]

    q1, q2, q3 = st.columns(3)

    with q1:
        grade = qrow.get("NAAC Grade", "")
        st.metric("NAAC Grade", str(grade) if str(grade) else "Not Available")

    with q2:
        cgpa_value = qrow.get("NAAC CGPA", "")
        if pd.notna(cgpa_value) and str(cgpa_value).strip():
            try:
                cgpa_number = float(cgpa_value)
                st.metric("NAAC CGPA", f"{cgpa_number:.2f}")
            except Exception:
                st.metric("NAAC CGPA", str(cgpa_value))
        else:
            st.metric("NAAC CGPA", "Not Available")

    with q3:
        nirf_rank = qrow.get("NIRF Rank", "")
        st.metric(
            "NIRF Rank",
            str(nirf_rank) if pd.notna(nirf_rank) and str(nirf_rank).strip() else "Not Available"
        )

    cgpa_raw = qrow.get("NAAC CGPA", "")
    try:
        cgpa_number = float(cgpa_raw)
        quality_score = cgpa_number / 4 * 100
        st.progress(min(max(quality_score / 100, 0), 1))
        st.caption(
            f"NAAC CGPA-based reference score: {quality_score:.1f}/100. "
            "This is a calculated reference score, not an official NAAC score."
        )
    except Exception:
        pass

    quality_display_columns = [
        "NAAC Grade",
        "NAAC CGPA",
        "NAAC Declaration Date",
        "NAAC Cycle",
        "NAAC Year",
        "NIRF Category",
        "NIRF Rank",
        "Placement Data",
        "Median Salary",
        "Fees",
        "Data Year"
    ]

    available_quality_columns = [
        column for column in quality_display_columns
        if column in quality_view.columns
    ]

    if available_quality_columns:
        st.dataframe(
            quality_view[available_quality_columns],
            use_container_width=True,
            hide_index=True
        )

    source_url = qrow.get("Source URL", "")
    if pd.notna(source_url) and str(source_url).strip():
        st.markdown(f"**Source:** {html.escape(str(source_url))}")

# =========================================================
# COLLEGE COMPARISON
# =========================================================

st.markdown("## ⚖️ College Comparison")

comparison_pool = display_results["InstituteName"].drop_duplicates().tolist() if not display_results.empty else []

if len(comparison_pool) >= 2:
    compare_options = comparison_pool[:100]

    selected_compare = st.multiselect(
        "Select 2 to 4 colleges",
        options=compare_options,
        max_selections=4,
        key="comparison_colleges"
    )

    if len(selected_compare) >= 2:
        comparison_rows = []

        for college_name in selected_compare:
            college_data = df[df["InstituteName"] == college_name]

            if college_data.empty:
                continue

            first = college_data.iloc[0]

            row_data = {
                "College": college_name,
                "State": first["State Name"],
                "District": first["District Name"],
                "Courses": len(college_data),
                "Programmes": college_data["Programme"].nunique(),
                "Disciplines": college_data["Discipline"].nunique(),
                "Modes": college_data["Mode"].nunique(),
            }

            matching_score = display_results[
                display_results["InstituteName"] == college_name
            ]["Match Score"]

            row_data["Match Score"] = (
                float(matching_score.max()) if not matching_score.empty else 0
            )

            comparison_rows.append(row_data)

        comparison_df = pd.DataFrame(comparison_rows)

        if not comparison_df.empty:
            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("Select at least 2 colleges to compare.")
else:
    st.info("Apply broader filters to get at least 2 colleges for comparison.")

# =========================================================
# ADVANCED ANALYTICS
# =========================================================

st.markdown("## 📊 Advanced Analytics")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Programme Analysis",
    "State Analysis",
    "District Analysis",
    "Mode Analysis",
    "College Search"
])

# ---------------------------------------------------------
# PROGRAMME ANALYSIS
# ---------------------------------------------------------

with tab1:
    programme_counts = results["Programme"].value_counts().head(12)

    if not programme_counts.empty:
        fig, ax = plt.subplots(figsize=(10, 5))

        programme_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Programme-wise Course Distribution")
        ax.set_xlabel("Programme")
        ax.set_ylabel("Number of Courses")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)


# ---------------------------------------------------------
# STATE ANALYSIS
# ---------------------------------------------------------

with tab2:
    state_counts = results["State Name"].value_counts().head(15)

    if not state_counts.empty:
        fig, ax = plt.subplots(figsize=(10, 5))

        state_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Top States by Course Availability")
        ax.set_xlabel("State")
        ax.set_ylabel("Number of Courses")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)


# ---------------------------------------------------------
# DISTRICT ANALYSIS
# ---------------------------------------------------------

with tab3:
    district_counts = results["District Name"].value_counts().head(15)

    if not district_counts.empty:
        fig, ax = plt.subplots(figsize=(10, 5))

        district_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Top Districts by Course Availability")
        ax.set_xlabel("District")
        ax.set_ylabel("Number of Courses")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)


# ---------------------------------------------------------
# MODE ANALYSIS
# ---------------------------------------------------------

with tab4:
    mode_counts = results["Mode"].value_counts()

    if not mode_counts.empty:
        fig, ax = plt.subplots(figsize=(8, 5))

        mode_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Course Availability by Mode")
        ax.set_xlabel("Mode")
        ax.set_ylabel("Number of Courses")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)


# ---------------------------------------------------------
# COLLEGE SEARCH
# ---------------------------------------------------------

with tab5:
    search_college = st.text_input(
        "Search College Name",
        placeholder="Enter college name..."
    )

    if search_college:
        college_search_results = results[
            results["InstituteName"]
            .str.contains(search_college, case=False, na=False)
        ]

        if not college_search_results.empty:
            st.dataframe(
                college_search_results,
                use_container_width=True
            )
        else:
            st.info("No matching college found.")

# =========================================================
# DATASET QUALITY
# =========================================================

st.markdown("## 🧪 Dataset Quality")

quality_cols = st.columns(4)

with quality_cols[0]:
    st.metric("Course Records", f"{len(df):,}")

with quality_cols[1]:
    st.metric("Unique Colleges", f"{df['InstituteName'].nunique():,}")

with quality_cols[2]:
    st.metric("States", f"{df['State Name'].nunique():,}")

with quality_cols[3]:
    st.metric("Disciplines", f"{df['Discipline'].nunique():,}")

missing_values = int(df.isna().sum().sum())

if missing_values == 0:
    st.success("✅ Main course dataset contains no missing values.")
else:
    st.warning(f"Dataset contains {missing_values:,} missing values.")

# =========================================================
# ABOUT
# =========================================================

st.markdown("## ℹ️ About the Project")

st.markdown("""
<div class="glass-card">
    <h3>🎓 Smart College Course Recommendation System</h3>
    <p>
        This platform helps students explore college courses and discover
        colleges based on their selected academic preferences.
    </p>
    <p>
        The system uses real college-course records and provides filtering,
        recommendation matching, college profiles, comparison, analytics,
        and available accreditation information.
    </p>
    <p>
        Recommendation percentages are preference-match scores generated
        from the selected filters. They are not official admission chances
        and do not represent an ML prediction.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🎓 Smart College Course Recommendation System
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:8px;
        margin-bottom:20px;
        color:#c4b5fd;
        font-size:14px;
        font-weight:500;
    ">
        Designed &amp; Developed by
        <strong style="
            font-size:22px;
            font-weight:900;
            letter-spacing:2.5px;
            margin-left:8px;
        ">
            VIRAJ DESAI
        </strong>
    </div>
    """,
    unsafe_allow_html=True
)