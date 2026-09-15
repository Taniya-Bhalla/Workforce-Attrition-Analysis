import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Workforce Attrition Analysis",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# DASHBOARD STYLING
# ============================================================

st.markdown("""
<style>

    /* ================= MAIN PAGE ================= */

    .stApp {
        background-color: #f5f7fb;
    }

    h1 {
        color: #0f172a !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #111827 !important;
        font-weight: 750 !important;
    }

    p {
        color: #1f2937;
    }


    /* ================= KPI CARDS ================= */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 16px;
        padding: 18px 15px;
        box-shadow: 0 5px 15px rgba(15, 23, 42, 0.08);
        transition: all 0.25s ease;
        min-height: 115px;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.18);
        border-color: #2563eb;
    }

    div[data-testid="stMetricLabel"] {
        color: #374151 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }

    div[data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 27px !important;
    }


    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0f172a 0%,
            #172554 50%,
            #1e293b 100%
        );
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }


    /* ================= SIDEBAR SELECTBOX ================= */

    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 2px solid #60a5fa !important;
        border-radius: 9px !important;
        min-height: 42px;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] div {
        color: #111827 !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] span {
        color: #111827 !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] input {
        color: #111827 !important;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] svg {
        fill: #2563eb !important;
    }


    /* ================= SIDEBAR SLIDER ================= */

    section[data-testid="stSidebar"] div[data-testid="stSlider"] {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSlider"] p {
        color: #ffffff !important;
    }


    /* ================= FILTER SUMMARY ================= */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ================= DIVIDERS ================= */

    hr {
        border-color: #dbe3ef !important;
    }


    /* ================= BUTTON / GENERAL ================= */

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("Palo Alto Networks.csv")


# ============================================================
# ATTRITION LABELS
# ============================================================

df["Attrition_Label"] = df["Attrition"].map({
    0: "Retained",
    1: "Exited"
})


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown("---")


# ---------------- DEPARTMENT ----------------

departments = ["All Departments"] + sorted(
    df["Department"].unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "🏢 Department",
    departments
)


# ---------------- JOB ROLE ----------------

roles = ["All Job Roles"] + sorted(
    df["JobRole"].unique().tolist()
)

selected_role = st.sidebar.selectbox(
    "👤 Job Role",
    roles
)


# ---------------- OVERTIME ----------------

overtime_options = ["All", "Yes", "No"]

selected_overtime = st.sidebar.selectbox(
    "⏰ Overtime",
    overtime_options
)


# ---------------- BUSINESS TRAVEL ----------------

travel_options = ["All"] + sorted(
    df["BusinessTravel"].unique().tolist()
)

selected_travel = st.sidebar.selectbox(
    "✈️ Business Travel",
    travel_options
)


# ---------------- TENURE RANGE ----------------

min_years = int(df["YearsAtCompany"].min())
max_years = int(df["YearsAtCompany"].max())

selected_tenure = st.sidebar.slider(
    "⏳ Years at Company",
    min_value=min_years,
    max_value=max_years,
    value=(min_years, max_years)
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_department != "All Departments":

    filtered_df = filtered_df[
        filtered_df["Department"] == selected_department
    ]


if selected_role != "All Job Roles":

    filtered_df = filtered_df[
        filtered_df["JobRole"] == selected_role
    ]


if selected_overtime != "All":

    filtered_df = filtered_df[
        filtered_df["OverTime"] == selected_overtime
    ]


if selected_travel != "All":

    filtered_df = filtered_df[
        filtered_df["BusinessTravel"] == selected_travel
    ]


filtered_df = filtered_df[
    (filtered_df["YearsAtCompany"] >= selected_tenure[0]) &
    (filtered_df["YearsAtCompany"] <= selected_tenure[1])
]


# ============================================================
# TITLE
# ============================================================

st.title(
    "📊 Workforce Attrition Patterns and Risk Hotspot Analysis"
)

st.markdown(
    "### Palo Alto Networks — Interactive HR Analytics Dashboard"
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_employees = len(filtered_df)

employees_exited = int(
    filtered_df["Attrition"].sum()
)

employees_retained = (
    total_employees - employees_exited
)


if total_employees > 0:

    attrition_rate = (
        employees_exited / total_employees
    ) * 100

else:

    attrition_rate = 0


# ---------------- EARLY TENURE ATTRITION ----------------

early_tenure = filtered_df[
    filtered_df["YearsAtCompany"] <= 3
]


if len(early_tenure) > 0:

    early_tenure_rate = (
        early_tenure["Attrition"].sum()
        / len(early_tenure)
    ) * 100

else:

    early_tenure_rate = 0


# ============================================================
# FIVE KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "👥 Total Employees",
    f"{total_employees:,}"
)


col2.metric(
    "📉 Attrition Rate",
    f"{attrition_rate:.2f}%"
)


col3.metric(
    "🚪 Employees Exited",
    f"{employees_exited:,}"
)


col4.metric(
    "✅ Employees Retained",
    f"{employees_retained:,}"
)


col5.metric(
    "⏳ Early-Tenure Attrition",
    f"{early_tenure_rate:.2f}%"
)


st.divider()


# ============================================================
# CURRENT FILTER SELECTION
# ============================================================

st.subheader("🔎 Current Filter Selection")

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)


summary_col1.write(
    f"**Department:** {selected_department}"
)


summary_col2.write(
    f"**Job Role:** {selected_role}"
)


summary_col3.write(
    f"**Overtime:** {selected_overtime}"
)


summary_col4.write(
    f"**Travel:** {selected_travel}"
)


# ============================================================
# ATTRITION DISTRIBUTION + EXITED PROFILE
# ============================================================

st.divider()

col_pie, col_profile = st.columns([2, 1])


# ---------------- ATTRITION DISTRIBUTION ----------------

with col_pie:

    st.subheader("📊 Attrition Distribution")

    attrition_counts = (
        filtered_df["Attrition_Label"]
        .value_counts()
        .reset_index()
    )

    attrition_counts.columns = [
        "Attrition",
        "Count"
    ]

    fig_pie = px.pie(
        attrition_counts,
        names="Attrition",
        values="Count",
        hole=0.45,
        title="Employees Retained vs Exited",
        color="Attrition",
        color_discrete_map={
            "Retained": "#2563eb",
            "Exited": "#60a5fa"
        }
    )

    fig_pie.update_traces(
        textinfo="percent",
        textfont_size=14
    )

    fig_pie.update_layout(
        height=450,
        legend_title="Status"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


# ---------------- EXITED EMPLOYEE PROFILE ----------------

with col_profile:

    st.subheader("👤 Exited Employee Profile")

    exited_employees = filtered_df[
        filtered_df["Attrition"] == 1
    ]


    if len(exited_employees) > 0:

        avg_age = exited_employees["Age"].mean()

        avg_tenure = exited_employees[
            "YearsAtCompany"
        ].mean()

        avg_distance = exited_employees[
            "DistanceFromHome"
        ].mean()

        avg_income = exited_employees[
            "MonthlyIncome"
        ].mean()


        st.metric(
            "Average Age",
            f"{avg_age:.1f} years"
        )


        st.metric(
            "Average Tenure",
            f"{avg_tenure:.1f} years"
        )


        st.metric(
            "Average Distance From Home",
            f"{avg_distance:.1f} km"
        )


        st.metric(
            "Average Monthly Income",
            f"${avg_income:,.0f}"
        )


    else:

        st.info(
            "No exited employees in the selected filters."
        )


# ============================================================
# DEPARTMENT & ROLE ANALYSIS
# ============================================================

st.divider()

st.header("🏢 Department & Role Analysis")

dept_col, role_col = st.columns(2)


# ---------------- DEPARTMENT ----------------

with dept_col:

    st.subheader("Department-wise Attrition")

    department_analysis = (
        filtered_df.groupby("Department")
        .agg(
            Total_Employees=("Attrition", "count"),
            Employees_Exited=("Attrition", "sum")
        )
        .reset_index()
    )

    department_analysis["Attrition_Rate"] = (
        department_analysis["Employees_Exited"]
        / department_analysis["Total_Employees"]
    ) * 100


    fig_department = px.bar(
        department_analysis,
        x="Department",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition Rate by Department",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_department.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_department.update_layout(
        yaxis_title="Attrition Rate (%)",
        xaxis_title="Department",
        coloraxis_showscale=False
    )


    st.plotly_chart(
        fig_department,
        use_container_width=True
    )


# ---------------- JOB ROLE ----------------

with role_col:

    st.subheader("Job Role-wise Attrition")

    role_analysis = (
        filtered_df.groupby("JobRole")
        .agg(
            Total_Employees=("Attrition", "count"),
            Employees_Exited=("Attrition", "sum")
        )
        .reset_index()
    )


    role_analysis["Attrition_Rate"] = (
        role_analysis["Employees_Exited"]
        / role_analysis["Total_Employees"]
    ) * 100


    role_analysis = role_analysis.sort_values(
        "Attrition_Rate",
        ascending=False
    )


    fig_role = px.bar(
        role_analysis,
        x="JobRole",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition Rate by Job Role",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_role.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_role.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Attrition Rate (%)",
        xaxis_title="Job Role",
        coloraxis_showscale=False
    )


    st.plotly_chart(
        fig_role,
        use_container_width=True
    )


# ============================================================
# HIGH-RISK AREAS
# ============================================================

st.subheader("🚨 High-Risk Areas")

risk_col1, risk_col2 = st.columns(2)


if not department_analysis.empty:

    highest_dept = department_analysis.loc[
        department_analysis["Attrition_Rate"].idxmax()
    ]


    with risk_col1:

        st.info(
            f"🏢 **Highest-Risk Department:** "
            f"{highest_dept['Department']} "
            f"({highest_dept['Attrition_Rate']:.2f}%)"
        )


if not role_analysis.empty:

    highest_role = role_analysis.iloc[0]


    with risk_col2:

        st.warning(
            f"👤 **Highest-Risk Job Role:** "
            f"{highest_role['JobRole']} "
            f"({highest_role['Attrition_Rate']:.2f}%)"
        )


# ============================================================
# DEMOGRAPHIC ATTRITION EXPLORER
# ============================================================

st.divider()

st.header("👥 Demographic Attrition Explorer")

demo_col1, demo_col2 = st.columns(2)


# ---------------- AGE GROUP ----------------

age_df = filtered_df.copy()


age_bins = [
    0,
    25,
    35,
    45,
    55,
    100
]


age_labels = [
    "Under 25",
    "25–34",
    "35–44",
    "45–54",
    "55+"
]


age_df["Age_Group"] = pd.cut(
    age_df["Age"],
    bins=age_bins,
    labels=age_labels,
    right=False
)


age_analysis = (
    age_df.groupby(
        "Age_Group",
        observed=False
    )
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


age_analysis["Attrition_Rate"] = (
    age_analysis["Employees_Exited"]
    / age_analysis["Total_Employees"]
) * 100


with demo_col1:

    st.subheader("Age Group")


    fig_age = px.bar(
        age_analysis,
        x="Age_Group",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Age Group",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_age.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_age.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Attrition Rate (%)"
    )


    st.plotly_chart(
        fig_age,
        use_container_width=True
    )


# ---------------- GENDER ----------------

gender_analysis = (
    filtered_df.groupby("Gender")
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


gender_analysis["Attrition_Rate"] = (
    gender_analysis["Employees_Exited"]
    / gender_analysis["Total_Employees"]
) * 100


with demo_col2:

    st.subheader("Gender")


    fig_gender = px.bar(
        gender_analysis,
        x="Gender",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Gender",
        color="Gender"
    )


    fig_gender.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_gender.update_layout(
        yaxis_title="Attrition Rate (%)"
    )


    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )


# ============================================================
# EDUCATION ANALYSIS
# ============================================================

st.divider()

st.header("🎓 Education Analysis")

edu_col1, edu_col2 = st.columns(2)


# ---------------- EDUCATION ----------------

education_analysis = (
    filtered_df.groupby("Education")
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


education_analysis["Attrition_Rate"] = (
    education_analysis["Employees_Exited"]
    / education_analysis["Total_Employees"]
) * 100


with edu_col1:

    st.subheader("Education")


    fig_education = px.bar(
        education_analysis,
        x="Education",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Education Level",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_education.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_education.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Attrition Rate (%)"
    )


    st.plotly_chart(
        fig_education,
        use_container_width=True
    )


# ---------------- EDUCATION FIELD ----------------

education_field_analysis = (
    filtered_df.groupby("EducationField")
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


education_field_analysis["Attrition_Rate"] = (
    education_field_analysis["Employees_Exited"]
    / education_field_analysis["Total_Employees"]
) * 100


with edu_col2:

    st.subheader("Education Field")


    fig_education_field = px.bar(
        education_field_analysis,
        x="EducationField",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Education Field",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_education_field.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_education_field.update_layout(
        xaxis_tickangle=-35,
        coloraxis_showscale=False,
        yaxis_title="Attrition Rate (%)"
    )


    st.plotly_chart(
        fig_education_field,
        use_container_width=True
    )


# ============================================================
# MARITAL STATUS
# ============================================================

st.divider()

st.subheader("💍 Marital Status")


marital_analysis = (
    filtered_df.groupby("MaritalStatus")
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


marital_analysis["Attrition_Rate"] = (
    marital_analysis["Employees_Exited"]
    / marital_analysis["Total_Employees"]
) * 100


fig_marital = px.bar(
    marital_analysis,
    x="MaritalStatus",
    y="Attrition_Rate",
    text="Attrition_Rate",
    title="Attrition by Marital Status",
    color="MaritalStatus"
)


fig_marital.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_marital.update_layout(
    yaxis_title="Attrition Rate (%)"
)


st.plotly_chart(
    fig_marital,
    use_container_width=True
)


# ============================================================
# TENURE & CAREER STAGE ANALYSIS
# ============================================================

st.divider()

st.header("⏳ Tenure & Career Stage Analysis")

tenure_col1, tenure_col2 = st.columns(2)


# ---------------- TENURE BUCKET ----------------

tenure_df = filtered_df.copy()


tenure_bins = [
    -1,
    3,
    6,
    10,
    20,
    100
]


tenure_labels = [
    "0–3 Years",
    "4–6 Years",
    "7–10 Years",
    "11–20 Years",
    "20+ Years"
]


tenure_df["Tenure_Bucket"] = pd.cut(
    tenure_df["YearsAtCompany"],
    bins=tenure_bins,
    labels=tenure_labels
)


tenure_analysis = (
    tenure_df.groupby(
        "Tenure_Bucket",
        observed=False
    )
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


tenure_analysis["Attrition_Rate"] = (
    tenure_analysis["Employees_Exited"]
    / tenure_analysis["Total_Employees"]
) * 100


with tenure_col1:

    st.subheader("Years at Company")


    fig_tenure = px.bar(
        tenure_analysis,
        x="Tenure_Bucket",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Tenure",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_tenure.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_tenure.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Attrition Rate (%)"
    )


    st.plotly_chart(
        fig_tenure,
        use_container_width=True
    )


# ---------------- YEARS SINCE PROMOTION ----------------

promotion_df = filtered_df.copy()


promotion_bins = [
    -1,
    1,
    3,
    5,
    10,
    100
]


promotion_labels = [
    "0–1 Years",
    "2–3 Years",
    "4–5 Years",
    "6–10 Years",
    "10+ Years"
]


promotion_df["Promotion_Bucket"] = pd.cut(
    promotion_df["YearsSinceLastPromotion"],
    bins=promotion_bins,
    labels=promotion_labels
)


promotion_analysis = (
    promotion_df.groupby(
        "Promotion_Bucket",
        observed=False
    )
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


promotion_analysis["Attrition_Rate"] = (
    promotion_analysis["Employees_Exited"]
    / promotion_analysis["Total_Employees"]
) * 100


with tenure_col2:

    st.subheader("Years Since Last Promotion")


    fig_promotion = px.bar(
        promotion_analysis,
        x="Promotion_Bucket",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition vs Promotion Gap",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_promotion.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_promotion.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Attrition Rate (%)"
    )


    st.plotly_chart(
        fig_promotion,
        use_container_width=True
    )


# ---------------- CAREER STAGE ----------------

career_df = filtered_df.copy()


career_df["Career_Stage"] = pd.cut(
    career_df["TotalWorkingYears"],
    bins=[-1, 5, 10, 100],
    labels=[
        "Early Career",
        "Mid Career",
        "Senior Career"
    ]
)


career_analysis = (
    career_df.groupby(
        "Career_Stage",
        observed=False
    )
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


career_analysis["Attrition_Rate"] = (
    career_analysis["Employees_Exited"]
    / career_analysis["Total_Employees"]
) * 100


st.subheader("🎓 Career Stage")


fig_career = px.bar(
    career_analysis,
    x="Career_Stage",
    y="Attrition_Rate",
    text="Attrition_Rate",
    title="Attrition by Career Stage",
    color="Career_Stage"
)


fig_career.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_career.update_layout(
    yaxis_title="Attrition Rate (%)"
)


st.plotly_chart(
    fig_career,
    use_container_width=True
)


# ============================================================
# WORKLOAD & MOBILITY ANALYSIS
# ============================================================

st.divider()

st.header("💼 Workload & Mobility Analysis")

work_col1, work_col2 = st.columns(2)


# ---------------- OVERTIME ----------------

overtime_analysis = (
    filtered_df.groupby("OverTime")
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


overtime_analysis["Attrition_Rate"] = (
    overtime_analysis["Employees_Exited"]
    / overtime_analysis["Total_Employees"]
) * 100


with work_col1:

    st.subheader("⏰ Overtime")


    fig_overtime = px.bar(
        overtime_analysis,
        x="OverTime",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Overtime",
        color="OverTime"
    )


    fig_overtime.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_overtime.update_layout(
        yaxis_title="Attrition Rate (%)"
    )


    st.plotly_chart(
        fig_overtime,
        use_container_width=True
    )


# ---------------- BUSINESS TRAVEL ----------------

travel_analysis = (
    filtered_df.groupby("BusinessTravel")
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


travel_analysis["Attrition_Rate"] = (
    travel_analysis["Employees_Exited"]
    / travel_analysis["Total_Employees"]
) * 100


with work_col2:

    st.subheader("✈️ Business Travel")


    fig_travel = px.bar(
        travel_analysis,
        x="BusinessTravel",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Business Travel",
        color="BusinessTravel"
    )


    fig_travel.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_travel.update_layout(
        yaxis_title="Attrition Rate (%)"
    )


    st.plotly_chart(
        fig_travel,
        use_container_width=True
    )


# ---------------- DISTANCE FROM HOME ----------------

distance_df = filtered_df.copy()


distance_df["Distance_Bucket"] = pd.cut(
    distance_df["DistanceFromHome"],
    bins=[-1, 5, 10, 20, 100],
    labels=[
        "0–5 km",
        "6–10 km",
        "11–20 km",
        "20+ km"
    ]
)


distance_analysis = (
    distance_df.groupby(
        "Distance_Bucket",
        observed=False
    )
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


distance_analysis["Attrition_Rate"] = (
    distance_analysis["Employees_Exited"]
    / distance_analysis["Total_Employees"]
) * 100


st.subheader("🏠 Distance From Home")


fig_distance = px.bar(
    distance_analysis,
    x="Distance_Bucket",
    y="Attrition_Rate",
    text="Attrition_Rate",
    title="Attrition by Distance From Home",
    color="Attrition_Rate",
    color_continuous_scale="Blues"
)


fig_distance.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)


fig_distance.update_layout(
    coloraxis_showscale=False,
    yaxis_title="Attrition Rate (%)"
)


st.plotly_chart(
    fig_distance,
    use_container_width=True
)


# ============================================================
# EMPLOYEE EXPERIENCE & COMPENSATION ANALYSIS
# ============================================================

st.divider()

st.header("😊 Employee Experience & Compensation Analysis")

experience_col1, experience_col2 = st.columns(2)


# ---------------- JOB SATISFACTION ----------------

satisfaction_analysis = (
    filtered_df.groupby("JobSatisfaction")
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


satisfaction_analysis["Attrition_Rate"] = (
    satisfaction_analysis["Employees_Exited"]
    / satisfaction_analysis["Total_Employees"]
) * 100


with experience_col1:

    st.subheader("😊 Job Satisfaction")


    fig_satisfaction = px.bar(
        satisfaction_analysis,
        x="JobSatisfaction",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Job Satisfaction",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_satisfaction.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_satisfaction.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Attrition Rate (%)",
        xaxis_title="Job Satisfaction (1–4)"
    )


    st.plotly_chart(
        fig_satisfaction,
        use_container_width=True
    )


# ---------------- MONTHLY INCOME ----------------

income_df = filtered_df.copy()


income_df["Income_Band"] = pd.cut(
    income_df["MonthlyIncome"],
    bins=[
        0,
        3000,
        6000,
        10000,
        float("inf")
    ],
    labels=[
        "Up to $3,000",
        "$3,001–$6,000",
        "$6,001–$10,000",
        "$10,000+"
    ],
    include_lowest=True
)


income_analysis = (
    income_df.groupby(
        "Income_Band",
        observed=False
    )
    .agg(
        Total_Employees=("Attrition", "count"),
        Employees_Exited=("Attrition", "sum")
    )
    .reset_index()
)


income_analysis["Attrition_Rate"] = (
    income_analysis["Employees_Exited"]
    / income_analysis["Total_Employees"]
) * 100


with experience_col2:

    st.subheader("💰 Monthly Income")


    fig_income = px.bar(
        income_analysis,
        x="Income_Band",
        y="Attrition_Rate",
        text="Attrition_Rate",
        title="Attrition by Monthly Income",
        color="Attrition_Rate",
        color_continuous_scale="Blues"
    )


    fig_income.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )


    fig_income.update_layout(
        coloraxis_showscale=False,
        yaxis_title="Attrition Rate (%)",
        xaxis_title="Monthly Income"
    )


    st.plotly_chart(
        fig_income,
        use_container_width=True
    )


# ============================================================
# ADDITIONAL ATTRITION INDICATORS
# ============================================================

st.divider()

st.header("📌 Additional Attrition Indicators")

indicator_col1, indicator_col2, indicator_col3 = st.columns(3)


# ---------------- WORKLOAD ATTRITION RATE ----------------

overtime_employees = filtered_df[
    filtered_df["OverTime"] == "Yes"
]


if len(overtime_employees) > 0:

    workload_attrition_rate = (
        overtime_employees["Attrition"].sum()
        / len(overtime_employees)
    ) * 100

else:

    workload_attrition_rate = 0


# ---------------- FREQUENT TRAVEL ATTRITION ----------------

frequent_travel = filtered_df[
    filtered_df["BusinessTravel"] == "Travel_Frequently"
]


if len(frequent_travel) > 0:

    frequent_travel_rate = (
        frequent_travel["Attrition"].sum()
        / len(frequent_travel)
    ) * 100

else:

    frequent_travel_rate = 0


# ---------------- EXITED EMPLOYEE AVG TENURE ----------------

if len(exited_employees) > 0:

    exited_avg_tenure = (
        exited_employees["YearsAtCompany"].mean()
    )

else:

    exited_avg_tenure = 0


indicator_col1.metric(
    "⏰ Overtime Attrition",
    f"{workload_attrition_rate:.2f}%"
)


indicator_col2.metric(
    "✈️ Frequent Travel Attrition",
    f"{frequent_travel_rate:.2f}%"
)


indicator_col3.metric(
    "📅 Exited Employee Avg. Tenure",
    f"{exited_avg_tenure:.1f} years"
)
# ============================================================
# KEY INSIGHTS & BUSINESS RECOMMENDATIONS
# ============================================================

st.divider()
st.header("💡 Key Insights & Business Recommendations")

# ---------------- DYNAMIC INSIGHT CALCULATIONS ----------------

highest_risk_department = None
highest_department_rate = 0

if not department_analysis.empty:
    highest_risk_department = department_analysis.loc[
        department_analysis["Attrition_Rate"].idxmax()
    ]
    highest_department_rate = float(
        highest_risk_department["Attrition_Rate"]
    )

highest_risk_role = None
highest_role_rate = 0

if not role_analysis.empty:
    highest_risk_role = role_analysis.iloc[0]
    highest_role_rate = float(
        highest_risk_role["Attrition_Rate"]
    )

highest_overtime = None
highest_overtime_rate = 0

if not overtime_analysis.empty:
    highest_overtime = overtime_analysis.loc[
        overtime_analysis["Attrition_Rate"].idxmax()
    ]
    highest_overtime_rate = float(
        highest_overtime["Attrition_Rate"]
    )

highest_travel = None
highest_travel_rate = 0

if not travel_analysis.empty:
    highest_travel = travel_analysis.loc[
        travel_analysis["Attrition_Rate"].idxmax()
    ]
    highest_travel_rate = float(
        highest_travel["Attrition_Rate"]
    )


# ---------------- INSIGHT CARDS ----------------

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    if highest_risk_department is not None:
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                padding:20px;
                border-radius:15px;
                border-left:6px solid #2563eb;
                box-shadow:0 4px 12px rgba(0,0,0,0.08);
                margin-bottom:15px;
            ">
                <h4 style="margin:0; color:#111827;">
                    🏢 Department Risk
                </h4>
                <p style="color:#374151; font-size:15px;">
                    <b>{highest_risk_department["Department"]}</b>
                    has the highest department-level attrition rate at
                    <b>{highest_department_rate:.2f}%</b>.
                    This area should receive focused retention attention.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

with insight_col2:

    if highest_risk_role is not None:
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                padding:20px;
                border-radius:15px;
                border-left:6px solid #dc2626;
                box-shadow:0 4px 12px rgba(0,0,0,0.08);
                margin-bottom:15px;
            ">
                <h4 style="margin:0; color:#111827;">
                    💼 Job Role Risk
                </h4>
                <p style="color:#374151; font-size:15px;">
                    <b>{highest_risk_role["JobRole"]}</b>
                    records the highest role-level attrition rate at
                    <b>{highest_role_rate:.2f}%</b>.
                    Targeted engagement and career-growth actions may help.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


insight_col3, insight_col4 = st.columns(2)

with insight_col3:

    if highest_overtime is not None:
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                padding:20px;
                border-radius:15px;
                border-left:6px solid #ea580c;
                box-shadow:0 4px 12px rgba(0,0,0,0.08);
                margin-bottom:15px;
            ">
                <h4 style="margin:0; color:#111827;">
                    ⏰ Overtime Risk
                </h4>
                <p style="color:#374151; font-size:15px;">
                    Employees working <b>{highest_overtime["OverTime"]}</b>
                    overtime show an attrition rate of
                    <b>{highest_overtime_rate:.2f}%</b>.
                    Workload balance should be monitored for this segment.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

with insight_col4:

    st.markdown(
        f"""
        <div style="
            background:#ffffff;
            padding:20px;
            border-radius:15px;
            border-left:6px solid #0891b2;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            margin-bottom:15px;
        ">
            <h4 style="margin:0; color:#111827;">
                🚀 Early-Tenure Risk
            </h4>
            <p style="color:#374151; font-size:15px;">
                Employees with <b>3 years or less</b> at the company show
                an attrition rate of <b>{early_tenure_rate:.2f}%</b>.
                Strong onboarding, mentoring and early-career engagement
                can support retention.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


insight_col5, insight_col6 = st.columns(2)

with insight_col5:

    if highest_travel is not None:
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                padding:20px;
                border-radius:15px;
                border-left:6px solid #16a34a;
                box-shadow:0 4px 12px rgba(0,0,0,0.08);
                margin-bottom:15px;
            ">
                <h4 style="margin:0; color:#111827;">
                    ✈️ Travel Risk
                </h4>
                <p style="color:#374151; font-size:15px;">
                    The <b>{highest_travel["BusinessTravel"]}</b> travel group
                    has the highest attrition rate at
                    <b>{highest_travel_rate:.2f}%</b>.
                    Travel demands should be considered in workforce planning.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

with insight_col6:

    st.markdown(
        """
        <div style="
            background:#ffffff;
            padding:20px;
            border-radius:15px;
            border-left:6px solid #7c3aed;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            margin-bottom:15px;
        ">
            <h4 style="margin:0; color:#111827;">
                🎯 Retention Strategy
            </h4>
            <p style="color:#374151; font-size:15px;">
                Prioritize high-risk departments and roles, review workload
                and travel demands, strengthen early-career support, and
                create clear development pathways for employees.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.header("📌 Project Information")

info_col1, info_col2 = st.columns(2)


with info_col1:

    st.markdown(
        """
        **📊 Project Title:**  
        Workforce Attrition Patterns and Risk Hotspot Analysis

        **🏢 Organization:**  
        Palo Alto Networks

        **🎯 Purpose:**  
        Data Analyst Internship Project

        **👩‍💻 Created By:**  
        Taniya

        **💼 Role:**  
        Data Analyst Intern
        """
    )


with info_col2:

    st.markdown(
        """
        **🛠️ Tools & Technologies:**  
        Python • Pandas • Streamlit • Plotly

        **📈 Analysis:**  
        Exploratory Data Analysis (EDA) • Attrition Analysis •
        Risk Hotspot Analysis

        **📊 Dashboard Type:**  
        Interactive HR Analytics Dashboard

        **🎯 Objective:**  
        To identify employee attrition patterns and
        high-risk workforce segments using data-driven insights.
        """
    )
# ============================================================
# DEVELOPER INFORMATION
# ============================================================

st.divider()

dev_col1, dev_col2, dev_col3 = st.columns([1, 2, 1])

with dev_col2:
    st.info(
        "👩‍💻  **Developed By Taniya**\n\n"
        "📊  **Data Analyst Intern**\n\n"
        "HR Analytics & Workforce Intelligence Project"
    )