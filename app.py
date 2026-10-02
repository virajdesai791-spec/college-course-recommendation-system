
import streamlit as st
import pandas as pd

# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Smart College Course Recommendation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD REAL AISHE DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("college_courses_combined.csv")

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    return df


data = load_data()

# =====================================================
# SESSION STATE
# =====================================================

if "search_started" not in st.session_state:
    st.session_state.search_started = False

# =====================================================
# HEADER
# =====================================================

st.title("🎓 Smart College Course Recommendation System")

st.write(
    "Discover colleges using real AISHE college-course data. "
    "Select your preferences, search for colleges and compare results."
)

st.divider()

# =====================================================
# DASHBOARD STATISTICS
# =====================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("📚 Course Records", f"{len(data):,}")
c2.metric("🏫 Unique Colleges", f"{data['AisheCode'].nunique():,}")
c3.metric("🇮🇳 States", data["State Name"].nunique())
c4.metric("🎓 Programmes", data["Programme"].nunique())
c5.metric("📖 Disciplines", data["Discipline"].nunique())

st.divider()

# =====================================================
# SIDEBAR: STUDENT PREFERENCES
# =====================================================

st.sidebar.title("🎯 Student Preferences")

marks = st.sidebar.number_input(
    "📊 Your Marks (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    step=0.1
)

st.sidebar.caption(
    "Marks are displayed for reference. They are not verified "
    "college admission cutoffs."
)

programmes = sorted(
    data.loc[data["Programme"] != "", "Programme"].unique()
)

programme = st.sidebar.selectbox(
    "🎓 Select Programme",
    programmes
)

programme_data = data[data["Programme"] == programme]

disciplines = sorted(
    programme_data.loc[
        programme_data["Discipline"] != "", "Discipline"
    ].unique()
)

discipline = st.sidebar.selectbox(
    "📚 Select Discipline",
    disciplines
)

states = sorted(
    data.loc[data["State Name"] != "", "State Name"].unique()
)

state = st.sidebar.selectbox(
    "📍 Preferred State",
    ["All States"] + states
)

if state != "All States":
    location_data = data[data["State Name"] == state]
else:
    location_data = data

districts = sorted(
    location_data.loc[
        location_data["District Name"] != "", "District Name"
    ].unique()
)

district = st.sidebar.selectbox(
    "🏙️ Preferred District",
    ["All Districts"] + districts
)

modes = sorted(
    data.loc[data["Mode"] != "", "Mode"].unique()
)

mode = st.sidebar.selectbox(
    "🏫 Study Mode",
    ["All Modes"] + modes
)

find_button = st.sidebar.button(
    "🚀 Find My Colleges",
    use_container_width=True
)

if find_button:
    st.session_state.search_started = True

# =====================================================
# HOME SCREEN
# =====================================================

if not st.session_state.search_started:

    st.subheader("Welcome to Your College Finder 🎓")

    a, b, c = st.columns(3)

    with a:
        st.info(
            "**Course Matching**\n\n"
            "Choose your programme and discipline to find colleges."
        )

    with b:
        st.info(
            "**Location Search**\n\n"
            "Filter colleges by state, district and study mode."
        )

    with c:
        st.info(
            "**College Search**\n\n"
            "Type a college name to display matching records only."
        )

    st.subheader("How It Works")

    st.write(
        "Select preferences → Filter real AISHE data → "
        "Search college names → View and download matching results."
    )

# =====================================================
# FIND AND DISPLAY COLLEGES
# =====================================================

if st.session_state.search_started:

    # -------------------------------------------------
    # FILTER PROGRAMME AND DISCIPLINE
    # -------------------------------------------------

    results = data[
        (data["Programme"] == programme)
        & (data["Discipline"].str.lower() == discipline.lower())
    ].copy()

    # -------------------------------------------------
    # FILTER STATE
    # -------------------------------------------------

    if state != "All States":
        results = results[results["State Name"] == state]

    # -------------------------------------------------
    # FILTER DISTRICT
    # -------------------------------------------------

    if district != "All Districts":
        results = results[results["District Name"] == district]

    # -------------------------------------------------
    # FILTER STUDY MODE
    # -------------------------------------------------

    if mode != "All Modes":
        results = results[results["Mode"] == mode]

    # One record per college, programme, discipline and mode
    results = results.drop_duplicates(
        subset=["AisheCode", "Programme", "Discipline", "Mode"]
    ).copy()

    st.subheader("🎯 Your Recommended Colleges")

    if results.empty:

        st.warning("No colleges found for these preferences.")

        st.info(
            "Try All Districts, another discipline, another state "
            "or a different study mode."
        )

    else:

        # -------------------------------------------------
        # COLLEGE SEARCH
        # IMPORTANT: results are recalculated on every rerun.
        # Session state keeps the results page open.
        # -------------------------------------------------

        st.subheader("🔎 Search for a College")

        search_college = st.text_input(
            "Type a college name",
            placeholder="Example: Sadguru Gadage Maharaj",
            key="college_search"
        )

        # Start from the selected course/location results
        display_results = results.copy()

        # Filter to only matching college names
        if search_college.strip():

            search_text = search_college.strip()

            display_results = display_results[
                display_results["InstituteName"].str.contains(
                    search_text,
                    case=False,
                    na=False,
                    regex=False
                )
            ].copy()

        # -------------------------------------------------
        # RECOMMENDATION SCORE
        # This is a preference-match score, NOT admission odds.
        # -------------------------------------------------

        if not display_results.empty:

            scores = pd.Series(
                60.0,
                index=display_results.index
            )

            if state != "All States":
                scores += 15

            if district != "All Districts":
                scores += 10

            if mode != "All Modes":
                scores += 10

            # Marks contribute at most 5 points.
            scores += marks * 0.05

            display_results["Recommendation Score"] = (
                scores.clip(upper=100).round(1)
            )

            display_results = display_results.sort_values(
                by="Recommendation Score",
                ascending=False
            )

        # -------------------------------------------------
        # RESULT COUNT AND MESSAGES
        # -------------------------------------------------

        st.metric(
            "🔎 Matching College-Course Records",
            f"{len(display_results):,}"
        )

        st.metric(
            "🏫 Unique Matching Colleges",
            f"{display_results['AisheCode'].nunique():,}"
        )

        if search_college.strip():

            if display_results.empty:
                st.warning(
                    f'No college found matching "{search_college}". '
                    "Try a shorter part of the college name."
                )
            else:
                st.success(
                    f'Found {display_results["AisheCode"].nunique():,} '
                    f'college(s) matching "{search_college}".'
                )
        else:
            st.success(
                f"Showing {len(display_results):,} matching "
                "college-course records."
            )

        # -------------------------------------------------
        # RESULTS TABLE
        # -------------------------------------------------

        if not display_results.empty:

            table_columns = [
                "AisheCode",
                "InstituteName",
                "State Name",
                "District Name",
                "Programme",
                "Discipline",
                "Mode",
                "Recommendation Score"
            ]

            st.dataframe(
                display_results[table_columns],
                use_container_width=True,
                hide_index=True
            )

            # -------------------------------------------------
            # DOWNLOAD MATCHING RESULTS
            # -------------------------------------------------

            csv_data = display_results[table_columns].to_csv(
                index=False
            )

            st.download_button(
                "📥 Download Matching Colleges (CSV)",
                data=csv_data,
                file_name="college_recommendations.csv",
                mime="text/csv",
                use_container_width=True
            )

            # -------------------------------------------------
            # TOP RECOMMENDATIONS
            # -------------------------------------------------

            st.divider()
            st.subheader("⭐ Top Matching Colleges")

            top_colleges = display_results.drop_duplicates(
                subset=["AisheCode"]
            ).head(5)

            for _, row in top_colleges.iterrows():

                st.markdown(f"### 🎓 {row['InstituteName']}")

                st.write(
                    f"**College Code:** {row['AisheCode']}  \n"
                    f"**State:** {row['State Name']}  \n"
                    f"**District:** {row['District Name']}  \n"
                    f"**Programme:** {row['Programme']}  \n"
                    f"**Discipline:** {row['Discipline']}  \n"
                    f"**Study Mode:** {row['Mode']}  \n"
                    f"**Preference-Match Score:** "
                    f"{row['Recommendation Score']}/100"
                )

                st.divider()

            # -------------------------------------------------
            # COLLEGE COMPARISON
            # -------------------------------------------------

            st.subheader("⚖️ Compare Colleges")

            college_options = (
                display_results[
                    ["AisheCode", "InstituteName"]
                ]
                .drop_duplicates(subset=["AisheCode"])
                .sort_values("InstituteName")
            )

            college_labels = {
                row["AisheCode"]: row["InstituteName"]
                for _, row in college_options.iterrows()
            }

            if len(college_labels) >= 2:

                selected_codes = st.multiselect(
                    "Select colleges to compare",
                    options=list(college_labels.keys()),
                    format_func=lambda code: college_labels[code],
                    max_selections=5,
                    key="compare_colleges"
                )

                if selected_codes:

                    comparison = display_results[
                        display_results["AisheCode"].isin(selected_codes)
                    ][table_columns].drop_duplicates()

                    st.dataframe(
                        comparison,
                        use_container_width=True,
                        hide_index=True
                    )

            else:
                st.caption(
                    "At least two matching colleges are needed for comparison."
                )

            # -------------------------------------------------
            # ANALYTICS
            # -------------------------------------------------

            st.divider()
            st.subheader("📊 Analysis of Matching Results")

            chart1, chart2 = st.columns(2)

            with chart1:
                st.write("**Colleges by State**")

                state_counts = (
                    display_results
                    .groupby("State Name")["AisheCode"]
                    .nunique()
                    .sort_values(ascending=False)
                    .head(10)
                )

                st.bar_chart(state_counts)

            with chart2:
                st.write("**Records by Study Mode**")

                mode_counts = (
                    display_results
                    .groupby("Mode")
                    .size()
                    .sort_values(ascending=False)
                )

                st.bar_chart(mode_counts)

            st.write("**Colleges by District**")

            district_counts = (
                display_results
                .groupby("District Name")["AisheCode"]
                .nunique()
                .sort_values(ascending=False)
                .head(10)
            )

            st.bar_chart(district_counts)

            # -------------------------------------------------
            # SEARCH PROFILE
            # -------------------------------------------------

            st.divider()
            st.subheader("📋 Your Search Profile")

            p1, p2, p3, p4 = st.columns(4)

            p1.write(f"**Marks:** {marks:.1f}%")
            p2.write(f"**Programme:** {programme}")
            p3.write(f"**Discipline:** {discipline}")
            p4.write(f"**Study Mode:** {mode}")

            # -------------------------------------------------
            # EXPLAIN SCORE AND DATA LIMITATIONS
            # -------------------------------------------------

            st.divider()
            st.subheader("🧠 How Recommendations Work")

            st.write(
                "First, the system filters the real AISHE records using "
                "your programme, discipline, state, district and study "
                "mode. It then assigns a transparent preference-match "
                "score to the remaining records."
            )

            st.info(
                "The score is not a college quality rating, admission "
                "probability or cutoff. Marks are displayed and included "
                "as a small score component, but the dataset does not "
                "contain verified college-wise admission cutoffs."
            )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Smart College Course Recommendation System | "
    "Python, Pandas and Streamlit | "
    "Based on the collected AISHE college-course dataset"
)

