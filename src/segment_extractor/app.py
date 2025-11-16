import tempfile
import json
from pathlib import Path

import streamlit as st

from io_img import load_img
from processing import get_border_points, points_to_segments, simplify_segments
from visualization import plot_points, plot_segments
from sorting import sort_segments

st.set_page_config(page_title="Segment Generator", layout="wide")
st.title("Segment Generator for SCARA drawing")

uploaded_file = st.file_uploader("Upload your image:", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file:
    tmp_path = Path(tempfile.gettempdir()) / uploaded_file.name
    tmp_path.write_bytes(uploaded_file.read())

    img = load_img(tmp_path)
    st.image(img, caption="Original Image", width="stretch")

    st.divider()

    st.subheader("Border Detection Parameters")
    t1 = st.slider("Threshold 1 (Canny)", 0, 255, 20)
    t2 = st.slider("Threshold 2 (Canny)", 0, 255, 50)

    st.subheader("Ramer-Douglas-Peucker Simplification Parameters")
    dist_threshold = st.slider("Radius of consideration between points", 1, 20, 5)
    eps = st.slider("ε RDP Parameter", 0.1, 10.0, 2.0)
    normalize_json = st.checkbox("Normalize points in JSON (0-1 range)", value=True)

    if st.button("Process Image"):
        st.subheader("Extracted Border")
        border_points = get_border_points(img, t1, t2)
        st.write(f"{len(border_points)} points")
        fig_points = plot_points(border_points, (10, 10))
        st.pyplot(fig_points)

        st.subheader("Extracted Segments")
        segments = points_to_segments(border_points, distance_threshold=dist_threshold)
        st.write(f"{len(segments)} segments")
        fig = plot_segments(segments, (10, 10))
        st.pyplot(fig)

        simple_segments = simplify_segments(segments, eps=eps, normalize=normalize_json)
        st.write(f"{sum(len(s) for s in simple_segments)} simplified points")
        st.write(f"{len(simple_segments)} simplified segments")
        fig = plot_segments(simple_segments, (10, 10))
        st.pyplot(fig)

        sorted_segments = sort_segments(simple_segments)
        json_obj = [s.to_json() for s in sorted_segments]
        json_data = json.dumps(json_obj)

        st.download_button(
            label="💾 Download JSON",
            data=json_data,
            file_name="segments.json",
            mime="application/json",
        )
