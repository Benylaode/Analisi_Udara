import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

data = pd.read_csv("data_udarah.csv")
data['datetime'] = pd.to_datetime(data['datetime'])

st.sidebar.header("Filter Data")
try:
    tanggal_input = st.sidebar.date_input("Rentang Tanggal", [data['datetime'].min(), data['datetime'].max()])
    if len(tanggal_input) == 2:
        mulai, selesai = tanggal_input
    else:
        mulai, selesai = data['datetime'].min(), data['datetime'].max()
except Exception as e:
    st.sidebar.error(f"Terjadi kesalahan pada input tanggal: {e}")
    mulai, selesai = data['datetime'].min(), data['datetime'].max()
station = st.sidebar.selectbox("Pilih Stasiun", data['station'].unique())
data_filter = data[(data['datetime'] >= pd.Timestamp(mulai)) &
                 (data['datetime'] <= pd.Timestamp(selesai)) &
                 (data['station'] == station)]

selected_parameters = st.sidebar.multiselect("Pilih Parameter", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'], default=['PM2.5'])

st.header("Dasbor Kualitas Udara")
st.subheader(f"Stasiun: {station}")

total_records = data_filter.shape[0]
st.metric("Jumlah Data", value=total_records)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=data_filter, x='datetime', y='Rata-Rata Kualitas Udarah', ax=ax)
ax.set_title("Tren Kualitas Udara")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Rata-Rata Kualitas Udara")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(12, 6))
kolom = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
for col in kolom:
    sns.lineplot(data=data_filter, x='datetime', y=col, ax=ax, label=col)
ax.set_title("Tren Kualitas Udara Berdasarkan Parameter")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Konsentrasi")
ax.legend(title="Parameter")
st.pyplot(fig)

st.caption("Data dari pengukuran kualitas udara.")

fig, ax = plt.subplots(figsize=(12, 6))
kolom = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
for col in selected_parameters:
    sns.lineplot(data=data_filter, x='datetime', y=col, ax=ax, label=col)
ax.set_title("Tren Kualitas Udara Berdasarkan Parameter")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Konsentrasi")
ax.legend(title="Parameter")
st.pyplot(fig)

st.caption("Data dari pengukuran kualitas udara.")

st.subheader("Heatmap Korelasi Parameter")
kolom_korelasi = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'Rata-Rata Kualitas Udarah']
korelasi_data = data_filter[kolom_korelasi].corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(korelasi_data, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.subheader("Penjelasan Parameter")
st.write("**TEMP:** Suhu udara dalam derajat Celcius.")
st.write("**PRES:** Tekanan udara dalam hPa.")
st.write("**DEWP:** Titik embun dalam derajat Celcius.")
st.write("**RAIN:** Curah hujan dalam mm.")
st.write("**WSPM:** Kecepatan angin dalam m/s.")
st.write("**PM2.5:** Partikel udara dengan diameter kurang dari 2.5 mikrometer.")
st.write("**PM10:** Partikel udara dengan diameter kurang dari 10 mikrometer.")
st.write("**SO2:** Konsentrasi sulfur dioksida.")
st.write("**NO2:** Konsentrasi nitrogen dioksida.")
st.write("**CO:** Konsentrasi karbon monoksida.")
st.write("**O3:** Konsentrasi ozon.")
st.write("**Rata-Rata Kualitas Udara:** Nilai agregat kualitas udara berdasarkan parameter di atas.")

