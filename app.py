import streamlit as st
import time
import csv
import os
import pandas as pd
from ultralytics import YOLO
from PIL import Image
from datetime import datetime

# Load trained model
model = YOLO("best.pt")

st.set_page_config(
    page_title="AI Smart Waste System",
    page_icon="♻",
    layout="centered"
)

# 🖤 Premium Dark Theme Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3, h4 {
        color: #00FFAA;
        text-align: center;
    }

    label {
        color: white !important;
    }

    .stButton>button {
        background-color: #00FFAA;
        color: black;
        border-radius: 8px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #00cc88;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1>♻ AI Powered Smart Waste Segregation System</h1>
    <p style='text-align:center;'>
    Smart Classification • Automated Bin Control • Location Logging
    </p>
""", unsafe_allow_html=True)

st.success("🌍 Promoting Sustainable Smart Cities Through AI")

st.divider()

# 📍 Location Section
st.subheader("📍 Location Details")
location = st.text_input("Enter Disposal Location")

# 📷 Image Section
st.subheader("📷 Capture or Upload Waste Image")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
camera_photo = st.camera_input("Or Take a Photo")

# Decide image source
image_file = None
if uploaded_file is not None:
    image_file = uploaded_file
elif camera_photo is not None:
    image_file = camera_photo

# Warning if no location
if image_file is not None and location.strip() == "":
    st.warning("⚠ Please enter location before proceeding.")

# 🚀 Main Processing
if image_file is not None and location.strip() != "":
    col1, col2 = st.columns(2)

    with col1:
        image = Image.open(image_file)
        st.image(image, caption="Captured Image", use_container_width=True)

    with col2:
        with st.spinner("🔍 AI is analyzing waste..."):
            time.sleep(1.5)
            results = model(image)

        predicted_class = results[0].names[results[0].probs.top1]
        confidence = float(results[0].probs.top1conf) * 100

        # ❌ Block Mixed Waste
        if predicted_class.lower() == "mixed":
            st.error("⚠ Mixed waste detected. Please separate waste properly.")
            st.stop()

        st.success(f"### 🗑 Waste Type: {predicted_class}")
        st.info(f"Confidence: {confidence:.2f}%")

        st.write("🚀 Activating Smart Bin...")
        time.sleep(2)
        st.success("Bin Opened ✅")
        time.sleep(6)
        st.info("Bin Closed")
        st.balloons()

    # 💾 Save History
    file_exists = os.path.isfile("history.csv")

    with open("history.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["DateTime", "Location", "Waste Type", "Confidence"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            location,
            predicted_class,
            f"{confidence:.2f}%"
        ])

    st.success("📁 Entry Saved Successfully")

st.divider()

# 📜 HISTORY SECTION
st.subheader("📜 Disposal History")

if st.checkbox("Show History"):
    if os.path.exists("history.csv"):
        df = pd.read_csv("history.csv")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Entries", len(df))
        col2.metric("Unique Locations", df["Location"].nunique())
        col3.metric("Waste Categories", df["Waste Type"].nunique())

        st.subheader("📊 Waste Summary")
        waste_count = df["Waste Type"].value_counts()
        st.bar_chart(waste_count)

        st.subheader("📋 Detailed Records")
        st.dataframe(df, use_container_width=True)

        if st.button("🗑 Clear History"):
            os.remove("history.csv")
            st.success("History Cleared Successfully!")
    else:
        st.warning("No history available yet.")

st.divider()

# Footer
st.markdown("""
    <hr>
    <center>
    <b>AI Smart Waste Segregation System</b><br>
    Built for Smart City Innovation Hackathon 2026 🚀
    </center>
""", unsafe_allow_html=True)
