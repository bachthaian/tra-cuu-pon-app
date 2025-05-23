
import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

@st.cache_data
def load_data():
    return pd.read_csv("points_data.csv")

@st.cache_data
def get_coordinates(address):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return None

def find_nearest_point(user_location, df):
    df["Khoảng cách (km)"] = df.apply(
        lambda row: geodesic(user_location, (row["Vĩ độ"], row["Kinh độ"])).km, axis=1
    )
    nearest = df.loc[df["Khoảng cách (km)"].idxmin()]
    return nearest

st.title("🔍 Tra cứu điểm PON gần nhất theo địa chỉ")

address_input = st.text_input("Nhập địa chỉ cần tra cứu:")

if address_input:
    coords = get_coordinates(address_input)
    if coords:
        df_points = load_data()
        nearest = find_nearest_point(coords, df_points)

        st.success("✅ Kết quả tra cứu:")
        st.write(f"**Địa chỉ nhập:** {address_input}")
        st.write(f"**Tọa độ:** {coords[0]:.6f}, {coords[1]:.6f}")
        st.write("---")
        st.write(f"**Mã tủ:** {nearest['Mã tủ']}")
        st.write(f"**Địa chỉ PON:** {nearest['Địa chỉ']}")
        st.write(f"**Vĩ độ:** {nearest['Vĩ độ']}")
        st.write(f"**Kinh độ:** {nearest['Kinh độ']}")
        st.write(f"**Khoảng cách:** {nearest['Khoảng cách (km)']:.2f} km")
    else:
        st.error("Không tìm thấy tọa độ từ địa chỉ nhập vào. Vui lòng kiểm tra lại.")

st.caption("© 2025 - Hệ thống tra cứu PON Huế")
