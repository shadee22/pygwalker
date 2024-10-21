from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)

# Add Title
st.title("Pygwalker-Streamlit")


# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
# Display link in light gray text if no file is uploaded
if uploaded_file is None:
    st.markdown('<small style="color: lightgray;">Default data is being used from <a href="https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv">kanaries dataset</a>.</small>', unsafe_allow_html=True)

# Cache the renderer to optimize memory usage
@st.cache_resource
def get_pyg_renderer(df: pd.DataFrame) -> "StreamlitRenderer":
    # If you want to use feature of saving chart config, set `spec_io_mode="rw"`
    return StreamlitRenderer(df, spec="./gw_config.json")

# Load default data or uploaded data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")

renderer = get_pyg_renderer(df)

# st.subheader("Display Explore UI")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["graphic walker", "data profiling", "graphic renderer", "pure chart", "table"]
)

with tab1:
    renderer.explorer()

with tab2:
    renderer.explorer(default_tab="data", key="explorer0")

with tab3:
    renderer.viewer()

with tab4:
    st.markdown("### Registered per weekday")

    # Check if there are enough charts in the renderer before trying to access them
    try:
        # Try rendering the first chart if it exists
        renderer.chart(0)
    except IndexError:
        st.error("Chart 0 not found or cannot be rendered.")

    st.markdown("### Registered per day")
    
    try:
        # Try rendering the second chart if it exists
        renderer.chart(1)
    except IndexError:
        st.error("Chart 1 not found or cannot be rendered.")

with tab5:
    try:
        # Display table if it exists
        renderer.table()
    except Exception as e:
        st.error(f"Error displaying the table: {e}")
