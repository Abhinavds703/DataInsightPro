import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="DataInsight Pro",
    page_icon="📊",
    layout="wide"
)

# ==================================
# HEADER
# ==================================
st.title("📊 DataInsight Pro")
st.subheader("Transform Raw Data into Smart Decisions")

st.write(
    "Upload any CSV file and get instant insights, data quality checks, and visual analytics."
)

st.divider()

# ==================================
# FILE UPLOAD
# ==================================
uploaded_file = st.file_uploader(
    "📁 Upload your CSV file",
    type=["csv"]
)

# ==================================
# MAIN APP
# ==================================
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("✅ Dataset Loaded Successfully!")

    rows = df.shape[0]
    columns = df.shape[1]
    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    # KPI CARDS
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", rows)
    col2.metric("Columns", columns)
    col3.metric("Missing Values", missing_values)
    col4.metric("Duplicate Rows", duplicate_rows)

    st.divider()

    # TABS
    tab1, tab2, tab3 = st.tabs(
        ["📊 Overview", "📈 Visualization", "🧹 Data Cleaning"]
    )

    # ==================================
    # OVERVIEW
    # ==================================
    with tab1:

        st.subheader("💚 Data Health Score")

        total_cells = rows * columns

        if total_cells > 0:
            health_score = round(
                ((total_cells - missing_values) / total_cells) * 100
            )
        else:
            health_score = 100

        st.metric(
            "Data Quality Score",
            f"{health_score}%"
        )

        if health_score >= 90:
            st.success("✅ Dataset is ready for analysis")
        elif health_score >= 70:
            st.warning("⚠️ Dataset needs minor cleaning")
        else:
            st.error("❌ Dataset needs cleaning")

        st.divider()

        # DATASET DOCTOR
        st.subheader("🩺 Dataset Doctor")

        issues = []

        if duplicate_rows > 0:
            issues.append(
                f"⚠️ {duplicate_rows} duplicate rows detected"
            )

        missing_by_column = df.isnull().sum()

        for col in missing_by_column.index:
            if missing_by_column[col] > 0:
                issues.append(
                    f"⚠️ Column '{col}' has {missing_by_column[col]} missing values"
                )

        if len(issues) == 0:
            st.success("✅ No major issues found in dataset")
        else:
            for issue in issues:
                st.warning(issue)

        st.divider()

        # SMART INSIGHTS
        st.subheader("🧠 Smart Insights")

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:

            for col in numeric_cols:

                avg_value = round(df[col].mean(), 2)

                st.write(
                    f"📊 {col}: Average = {avg_value} | Min = {df[col].min()} | Max = {df[col].max()}"
                )

        else:
            st.info("No numeric columns found.")

        st.divider()

        # AI FINDINGS
        st.subheader("🤖 AI Findings")

        findings = []

        if "Age" in df.columns:
            avg_age = df["Age"].mean()

            if avg_age > 40:
                findings.append(
                    "⚠️ Average age is above 40 years."
                )
            else:
                findings.append(
                    "✅ Average age is relatively healthy."
                )

        if "Cholesterol" in df.columns:
            avg_chol = df["Cholesterol"].mean()

            if avg_chol > 200:
                findings.append(
                    "⚠️ Average cholesterol level is above healthy range."
                )
            else:
                findings.append(
                    "✅ Cholesterol level looks healthy."
                )

        if "Heart_Rate" in df.columns:
            avg_hr = df["Heart_Rate"].mean()

            if avg_hr > 80:
                findings.append(
                    "⚠️ Average heart rate is slightly elevated."
                )
            else:
                findings.append(
                    "✅ Heart rate values are normal."
                )

        if missing_values == 0:
            findings.append(
                "✅ No missing values detected."
            )

        if duplicate_rows == 0:
            findings.append(
                "✅ No duplicate rows detected."
            )

        for item in findings:
            st.write(item)

        st.divider()

        # RISK SCORE
        st.subheader("🏥 Dataset Risk Score")

        risk_score = 0

        if "Age" in df.columns and df["Age"].mean() > 40:
            risk_score += 20

        if "Cholesterol" in df.columns and df["Cholesterol"].mean() > 200:
            risk_score += 40

        if "Heart_Rate" in df.columns and df["Heart_Rate"].mean() > 80:
            risk_score += 20

        if missing_values > 0:
            risk_score += 10

        if duplicate_rows > 0:
            risk_score += 10

        risk_score = min(risk_score, 100)

        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

        if risk_score < 30:
            st.success("🟢 Low Risk Dataset")
        elif risk_score < 70:
            st.warning("🟡 Medium Risk Dataset")
        else:
            st.error("🔴 High Risk Dataset")

        st.divider()

        st.subheader("📋 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

    # ==================================
    # VISUALIZATION
    # ==================================
    with tab2:

        st.subheader("📈 Smart Visualizations")

        numeric_cols = df.select_dtypes(
            include=["number"]
        ).columns

        if len(numeric_cols) > 0:

            selected_col = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig_bar = px.bar(
                df,
                y=selected_col,
                title=f"{selected_col} Analysis"
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

            fig_hist = px.histogram(
                df,
                x=selected_col,
                title=f"{selected_col} Distribution"
            )

            st.plotly_chart(
                fig_hist,
                use_container_width=True
            )

        else:
            st.warning(
                "No numeric columns found."
            )

    # ==================================
    # DATA CLEANING
    # ==================================
    with tab3:

        st.subheader("🧹 Data Cleaning")

        cleaned_df = df.copy()

        st.write("Remove duplicate rows from dataset.")

        if st.button("🗑 Remove Duplicate Rows"):

            before_rows = cleaned_df.shape[0]

            cleaned_df = cleaned_df.drop_duplicates()

            after_rows = cleaned_df.shape[0]

            removed = before_rows - after_rows

            st.success(
                f"✅ {removed} duplicate rows removed successfully!"
            )

            st.dataframe(
                cleaned_df,
                use_container_width=True
            )

            csv = cleaned_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 Download Clean Dataset",
                data=csv,
                file_name="clean_dataset.csv",
                mime="text/csv"
            )

# ==================================
# FOOTER
# ==================================
st.divider()

st.markdown(
    """
    <center>
    <small>Powered by DataInsight Pro • Developed by Abhinav Singh</small>
    </center>
    """,
    unsafe_allow_html=True
)