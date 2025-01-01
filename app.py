import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
import json

# Function to load Lottie animations
def load_lottie_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

# Load animations
college_animation = load_lottie_file("college_animation.json")
branch_animation = load_lottie_file("branch_animation.json")

# Define the file path
FILE_PATH = "cet_matrix.xlsx"

# Custom CSS for background and font
st.markdown(
    """
    <style>
    body {
        background-image: url('https://img.freepik.com/premium-vector/education-student-school-background-pattern-design_260839-73.jpg?semt=ais_hybrid');
        background-size: cover;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px 20px;
    }
    .stSelectbox {
        font-size: 16px;
    }
    .tabs-container {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }
    .custom-header {
        text-align: center;
        color: #4CAF50;
        font-weight: bold;
        font-size: 2.5rem;
        text-shadow: 2px 2px #000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load the Excel file with a progress bar
@st.cache_data
def load_excel_file():
    """Load Excel file."""
    with st.spinner("Loading data... Please wait"):
        try:
            data = pd.read_excel(FILE_PATH, engine="openpyxl")
            data.columns = data.columns.str.strip()  # Remove leading/trailing spaces
            return data
        except FileNotFoundError:
            st.error("The file 'cet_matrix.xlsx' was not found. Please check the file path.")
            return None
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return None

# Load data
df = load_excel_file()

# Fallback order dictionary
fallback_order = {
    "1R": ["1R", "1G", "GM"],
    "1K": ["1K", "1G", "GM"],
    "1G": ["1G", "GM"],
    "2AR": ["2AR", "2AG", "GM"],
    "2AK": ["2AK", "2AG", "GM"],
    "2AG": ["2AG", "GM"],
    "2BR": ["2BR", "2BG", "GM"],
    "2BK": ["2BK", "2BG", "GM"],
    "2BG": ["2BG", "GM"],
    "3AK": ["3AK", "3AG", "GM"],
    "3AR": ["3AR", "3AG", "GM"],
    "3AG": ["3AG", "GM"],
    "3BK": ["3BK", "3BG", "GM"],
    "3BR": ["3BR", "3BG", "GM"],
    "3BG": ["3BG", "GM"],
    "STK": ["STK", "STG", "GM"],
    "STR": ["STR", "STG", "GM"],
    "STG": ["STG", "GM"],
    "SCK": ["SCK", "SCG", "GM"],
    "SCR": ["SCR", "SCG", "GM"],
    "SCG": ["SCG", "GM"],
    "GMR": ["GMR", "GM"],
    "GMK": ["GMK", "GM"],
    "GM": ["GM"]
}

# App Title with Animation
st.title("🎓 K-CET Counselling Helper")
st_lottie(college_animation, height=300, key="college_anim")
st.write("### 🔍 Explore Seat Matrix and Make Informed Choices")

# Collapsible disclaimer section
with st.expander("📢 **Disclaimer**"):
    st.write(
        """
        - The seat matrix displayed is based on available data.
        - Actual results may vary during counselling.
        - Use this app for reference and decision-making.
        """
    )

# Dropdown and tab section
st.write("---")  # Separator line for better layout
col1, col2 = st.columns([1, 2])
with col1:
    exclusion_list = ["College Code", "Place", "College Name", "Branch Name", "Branch code", "SNQ", "Total"]
    category_list = [col for col in df.columns if col not in exclusion_list]
    selected_category = st.selectbox("📊 Select Category", ["--Select--"] + sorted(category_list), key="add_category")

# Tabs
st.write("---")
tabs = st.tabs(["🏫 College Analysis"])

# Tab 1: College Analysis
with tabs[0]:
    st.write("#### 🏅 Explore Particular Colleges")
    st_lottie(branch_animation, height=200, key="branch_anim")
    selected_college = st.selectbox(
        "🔽 Select College",
        ["--Select--"] + sorted(df["College Name"].dropna().unique()),
        disabled=(selected_category == "--Select--"),
        key="add_college",
    )

    if selected_college != "--Select--" and selected_category != "--Select--":
        fallback_categories = fallback_order.get(selected_category, [selected_category])
        filtered_data = df[(df["College Name"] == selected_college) & (df[fallback_categories].any(axis=1))]

        if not filtered_data.empty:
            st.success(f"🎓 Showing seat matrix for **{selected_category}** in **{selected_college}**:")
            filtered_data = filtered_data.reset_index(drop=True)
            filtered_data.index = range(1, len(filtered_data) + 1)
            st.table(filtered_data[["Branch Name"] + fallback_categories + ["SNQ", "Total"]])
        else:
            st.error("🚫 No data available for the selected category and college.")

# Tab 2: Branch Analysis
# with tabs[1]:
#     st.write("#### 🏅 Explore All Colleges")
#     if selected_category != "--Select--":
#         fallback_categories = fallback_order.get(selected_category, [selected_category])
#         all_colleges_data = df[["College Name", "Branch Name"] + fallback_categories + ["SNQ", "Total"]]

#         st.success(f"Displaying seat matrix for **{selected_category}** across all colleges:")
#         st.dataframe(all_colleges_data)
