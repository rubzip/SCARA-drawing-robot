import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import tempfile
import json
from pathlib import Path

from io_img import load_img, save_segment_image
from processing import get_border_points, points_to_segments_kdtree, simplify_segments
from visualization import plot_segments

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
    t1 = st.slider("Threshold 1 (Canny)", 0, 255, 50)
    t2 = st.slider("Threshold 2 (Canny)", 0, 255, 150)

    st.subheader("Ramer-Douglas-Peucker Simplification Parameters")
    dist_threshold = st.slider("Radius of consideration between points", 1, 20, 5)
    eps = st.slider("ε RDP Parameter", 0.1, 10.0, 2.0)

    if st.button("Process Image"):
        border_points = get_border_points(img, t1, t2)
        st.write(f"{len(border_points)} points")

        segments = points_to_segments_kdtree(border_points, distance_threshold=dist_threshold)
        st.write(f"{len(segments)} segments")

        simple_segments = simplify_segments(segments)
        st.write(f"{sum(len(s) for s in simple_segments)} simplified points")

        fig = plot_segments(simple_segments, (10, 10))
        st.pyplot(fig)

        json_obj = [s.to_json() for s in simple_segments]
        json_data = json.dumps(json_obj)

        st.download_button(
            label="💾 Descargar fichero JSON",
            data=json_data,
            file_name="segments.json",
            mime="application/json"
        )
