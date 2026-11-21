# ============================================================
# AUDITFIT v1.1 (Streamlit)
# Auditor Soundness Assessment
# Run locally:  streamlit run app.py
# ============================================================

from html import escape

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AuditFit",
    page_icon="📊",
    layout="centered",
)

# ============================================================
# 1. SCORING ENGINE
# ============================================================

def experience_score(years):
    if years < 1:
        return 0
    elif years < 3:
        return 40
    elif years < 5:
        return 60
    elif years < 10:
        return 80
    return 100


def project_score(projects):
    if projects == 0:
        return 0
    elif projects == 1:
        return 25
    elif projects <= 3:
        return 50
    elif projects <= 5:
        return 75
    return 100


def expertise_score(level):
    scores = {
        "Basic": 25,
        "Intermediate": 50,
        "Advanced": 75,
        "Expert": 100,
    }
    return scores[level]


def calculate_rating(years, level, projects, certification):

    exp = experience_score(years)
    expert = expertise_score(level)
    proj = project_score(projects)
    cert = 100 if certification else 0

    # Weighted scoring model
    total = (
        exp * 0.25
        + expert * 0.30
        + proj * 0.30
        + cert * 0.15
    )

    # Rating classification
    if total >= 85:
        rating = "HIGHLY FIT"
        recommendation = "Suitable for senior audit assignments."
    elif total >= 70:
        rating = "FIT"
        recommendation = "Suitable for regular audit assignments."
    elif total >= 50:
        rating = "CONDITIONALLY FIT"
        recommendation = "Additional supervision and competency development are recommended."
    else:
        rating = "NOT YET FIT"
        recommendation = "Further competency development is required."

    return {
        "Experience": exp,
        "Expertise": expert,
        "Projects": proj,
        "Certification": cert,
        "Total": round(total, 1),
        "Rating": rating,
        "Recommendation": recommendation,
    }


# ============================================================
# 2. DASHBOARD HTML BUILDER
# ============================================================

RATING_COLORS = {
    "HIGHLY FIT": "#15803d",
    "FIT": "#16a34a",
    "CONDITIONALLY FIT": "#d97706",
    "NOT YET FIT": "#dc2626",
}

WEIGHTS = {
    "Experience": 25,
    "Expertise": 30,
    "Projects": 30,
    "Certification": 15,
}


def build_dashboard(auditor_name, domain, years, level, projects, certification, result):

    color = RATING_COLORS[result["Rating"]]

    # Score breakdown rows
    rows = ""
    for item, weight in WEIGHTS.items():
        score = result[item]
        weighted = score * weight / 100

        rows += f"""
        <tr>
            <td style="padding:14px 10px;"><b>{item}</b></td>
            <td style="text-align:center;">{score}/100</td>
            <td style="text-align:center;">{weight}%</td>
            <td style="text-align:center;"><b>{weighted:.1f}</b></td>
            <td style="width:30%;padding:10px;">
                <div style="background:#e5e7eb;border-radius:10px;height:12px;">
                    <div style="background:#16a34a;width:{score}%;height:12px;border-radius:10px;"></div>
                </div>
            </td>
        </tr>
        """

    return f"""
    <div style="
        width:100%;
        box-sizing:border-box;
        font-family:Arial,sans-serif;
        padding:24px;
        border:1px solid #ddd;
        border-radius:14px;
        background:white;
        color:#222;
    ">

        <h1 style="margin:0;color:#166534;font-size:30px;">AuditFit</h1>

        <p style="color:#666;margin-top:5px;">Auditor Soundness Assessment Report</p>

        <hr style="border:0;border-top:1px solid #ddd;">

        <h3>1. Auditor Profile</h3>

        <table style="width:100%;border-collapse:collapse;font-size:14px;">
            <tr>
                <td style="padding:10px;"><b>Auditor Name</b></td>
                <td>{escape(auditor_name)}</td>
                <td><b>Expertise</b></td>
                <td>{escape(domain)}</td>
            </tr>
            <tr>
                <td style="padding:10px;"><b>Experience</b></td>
                <td>{years} years</td>
                <td><b>Level</b></td>
                <td>{escape(level)}</td>
            </tr>
            <tr>
                <td style="padding:10px;"><b>Projects</b></td>
                <td>{projects}</td>
                <td><b>Certification</b></td>
                <td>{"Yes" if certification else "No"}</td>
            </tr>
        </table>

        <br>

        <h3>2. Soundness Assessment</h3>

        <div style="background:#f0fdf4;padding:25px;border-radius:12px;text-align:center;">
            <div style="font-size:14px;color:#555;">TOTAL SOUNDNESS SCORE</div>
            <div style="font-size:56px;font-weight:bold;color:{color};margin:10px;">
                {result["Total"]}/100
            </div>
            <span style="
                background:{color};
                color:white;
                padding:10px 28px;
                border-radius:25px;
                font-weight:bold;
                font-size:15px;
            ">
                {result["Rating"]}
            </span>
        </div>

        <br>

        <h3>3. Score Breakdown</h3>

        <table style="width:100%;border-collapse:collapse;font-size:14px;">
            <thead style="background:#f3f4f6;">
                <tr>
                    <th style="padding:12px;text-align:left;">Dimension</th>
                    <th>Score</th>
                    <th>Weight</th>
                    <th>Weighted Score</th>
                    <th>Performance</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <br>

        <h3>4. Assessment Recommendation</h3>

        <div style="
            background:#f9fafb;
            padding:18px;
            border-left:5px solid {color};
            border-radius:5px;
            font-size:15px;
        ">
            {result["Recommendation"]}
        </div>

        <br>

        <div style="
            color:#888;
            font-size:12px;
            text-align:center;
            border-top:1px solid #ddd;
            padding-top:15px;
        ">
            AuditFit v1.1 | Rule-Based Assessment | For Demonstration Purposes
        </div>

    </div>
    """


# ============================================================
# 3. APPLICATION INTERFACE
# ============================================================

st.markdown(
    "<h1 style='color:#166534;margin-bottom:0;'>📊 AuditFit</h1>"
    "<p style='color:gray;font-size:16px;margin-top:0;'>Auditor Soundness Assessment</p>",
    unsafe_allow_html=True,
)

st.subheader("1. Auditor Profile")

auditor_name = st.text_input("Name", placeholder="Enter auditor name")
years = st.slider("Experience (years)", min_value=0, max_value=30, value=5)

st.subheader("2. Competency")

domain = st.selectbox("Expertise", ["IT", "Finance", "Fraud", "Risk Management"], index=0)
level = st.selectbox("Level", ["Basic", "Intermediate", "Advanced", "Expert"], index=2)
projects = st.slider("Projects", min_value=0, max_value=20, value=3)
certification = st.checkbox("Has relevant professional certification", value=True)

assess = st.button("✅ ASSESS AUDITOR", type="primary", use_container_width=True)

# ============================================================
# 4. ASSESSMENT DASHBOARD
# ============================================================

if assess:
    if not auditor_name.strip():
        st.error("Please enter auditor name.")
    else:
        result = calculate_rating(years, level, projects, certification)
        dashboard = build_dashboard(
            auditor_name, domain, years, level, projects, certification, result
        )
        components.html(dashboard, height=980, scrolling=True)

# ============================================================
# 5. SCORING METHODOLOGY
# ============================================================

with st.expander("View Scoring Methodology"):
    st.markdown(
        """
**Weight Distribution**
- Experience: 25%
- Expertise: 30%
- Project Exposure: 30%
- Certification: 15%

**Rating Classification**
- 85-100: Highly Fit
- 70-84: Fit
- 50-69: Conditionally Fit
- Below 50: Not Yet Fit
"""
    )

# ============================================================
# END OF AUDITFIT v1.1
# ============================================================
