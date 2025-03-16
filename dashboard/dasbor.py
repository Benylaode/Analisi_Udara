import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

data = pd.read_csv("data_udarah.csv")
data['datetime'] = pd.to_datetime(data['datetime'])

st.sidebar.header("Filter Data")
tanggal_input = st.sidebar.date_input("Rentang Tanggal", [data['datetime'].min(), data['datetime'].max()])
if len(tanggal_input) == 2:
    mulai, selesai = tanggal_input
else:
    mulai, selesai = data['datetime'].min(), data['datetime'].max()

station = st.sidebar.selectbox("Pilih Stasiun", data['station'].unique())
selected_parameters = st.sidebar.multiselect("Pilih Parameter", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'], default=['PM2.5'])
view_option = st.sidebar.radio("Pilih Tampilan", ["Rata-rata per Stasiun", "Rata-rata per Tahun", "Rata-rata sesuai Rentang"])

data_filter = data[(data['datetime'] >= pd.Timestamp(mulai)) &
                    (data['datetime'] <= pd.Timestamp(selesai)) &
                    (data['station'] == station)]

st.header("Dasbor Kualitas Udara")
st.subheader(f"Stasiun: {station}")

total_records = data_filter.shape[0]
st.metric("Jumlah Data", value=total_records)

fig, ax = plt.subplots(figsize=(12, 6))
for col in selected_parameters:
    sns.lineplot(data=data_filter, x='datetime', y=col, ax=ax, label=col)
ax.set_title("Tren Kualitas Udara Berdasarkan Parameter")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Konsentrasi")
ax.legend(title="Parameter")
st.pyplot(fig)

if view_option == "Rata-rata per Stasiun":
    station_avg = data.groupby("station")[selected_parameters].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    station_avg.plot(kind='bar', ax=ax, colormap='coolwarm')
    ax.set_title("Rata-rata Kualitas Udara per Stasiun")
    ax.set_xlabel("Stasiun")
    ax.set_ylabel("Konsentrasi")
    st.pyplot(fig)

elif view_option == "Rata-rata per Tahun":
    data['year'] = data['datetime'].dt.year
    yearly_avg = data.groupby("year")[selected_parameters].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    yearly_avg.plot(kind='bar', ax=ax, colormap='viridis')
    ax.set_title("Rata-rata Kualitas Udara per Tahun")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Konsentrasi")
    st.pyplot(fig)

elif view_option == "Rata-rata sesuai Rentang":
    range_avg = data_filter[selected_parameters].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    range_avg.plot(kind='bar', ax=ax, color='teal')
    ax.set_title("Rata-rata Kualitas Udara dalam Rentang Waktu Dipilih")
    ax.set_xlabel("Parameter")
    ax.set_ylabel("Konsentrasi")
    st.pyplot(fig)

st.subheader("Heatmap Korelasi Parameter")
kolom_korelasi = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM'] + selected_parameters
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


