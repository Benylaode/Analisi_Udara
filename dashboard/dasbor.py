import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

data = pd.read_csv("data_udarah.csv")
data['datetime'] = pd.to_datetime(data['datetime'])
data['year'] = data['datetime'].dt.year

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

df_avg = data.groupby("station")[selected_parameters].mean()
if view_option == "Rata-rata per Stasiun":
    fig, ax = plt.subplots(figsize=(12, 6))
    df_avg.plot(kind='bar', ax=ax, colormap='coolwarm')
    ax.set_title("Rata-rata Kualitas Udara per Stasiun")
    st.pyplot(fig)

elif view_option == "Rata-rata per Tahun":
    df_yearly = data.groupby("year")[selected_parameters].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    df_yearly.plot(kind='bar', ax=ax, colormap='viridis')
    ax.set_title("Rata-rata Kualitas Udara per Tahun")
    st.pyplot(fig)

elif view_option == "Rata-rata sesuai Rentang":
    range_avg = data_filter[selected_parameters].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    range_avg.plot(kind='bar', ax=ax, color='teal')
    ax.set_title("Rata-rata Kualitas Udara dalam Rentang Waktu Dipilih")
    st.pyplot(fig)

data_2016 = data[data['year'] == 2016]
stasiun_terburuk = data_2016.groupby("station")['Rata-Rata Kualitas Udarah'].mean().idxmax()
st.metric("Stasiun dengan Kualitas Udara Terburuk (2016)", value=stasiun_terburuk)

df_avg_2016 = data[data["year"] == 2016].groupby("station")["Rata-Rata Kualitas Udarah"].mean()

max_value = df_avg_2016.max()
max_station = df_avg_2016.idxmax()

stations = list(df_avg_2016.index)
max_index = stations.index(max_station)
colors = ["red" if station == max_station else "blue" for station in df_avg_2016.index]

fig, ax = plt.subplots(figsize=(12, 6))
df_avg_2016.plot(kind='bar', ax=ax, color=colors)
ax.set_title("Rata-Rata Kualitas Udarah per Stasiun pada rentang 2016")
ax.set_ylabel("Rata-Rata Kualitas Udarah")
ax.set_xlabel("Stasiun")

ax.text(max_index, max_value, f"{max_value:.2f}", ha='center', va='bottom', fontsize=12, fontweight='bold', color='red')
st.pyplot(fig)



jumlah_data_per_tahun = data.groupby("year")['Rata-Rata Kualitas Udarah'].count()
print(jumlah_data_per_tahun)
tahun_lengkap = jumlah_data_per_tahun[jumlah_data_per_tahun >= 73210].index
df_filtered = data[data["year"].isin(tahun_lengkap)].groupby("year")['Rata-Rata Kualitas Udarah'].mean()
tahun_terburuk = df_filtered.idxmax()

st.metric("Tahun dengan Kualitas Udara Terburuk (hany menampilkan data yang lengkap satu tahun)", value=tahun_terburuk)
colors = ['gray'] * len(df_filtered)
colors[df_filtered.index.get_loc(tahun_terburuk)] = 'red'
fig, ax = plt.subplots(figsize=(12, 6))
df_filtered.plot(kind='bar', ax=ax, colormap='viridis', color=colors)
ax.set_title("Rata-Rata Kualitas Udarah per Tahun")
ax.set_ylabel("Konsentrasi")
for i, val in enumerate(df_filtered):
    ax.text(i, val, f"{val:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')


st.pyplot(fig)

st.subheader("Heatmap Korelasi Parameter")

kolom_sebab= ["TEMP","PRES","DEWP","RAIN", "WSPM", "Rata-Rata Kualitas Udarah" ]
korelasi_data = data[kolom_sebab].corr()
korelasi_rata2 = korelasi_data['Rata-Rata Kualitas Udarah'].drop("Rata-Rata Kualitas Udarah").abs()

korelasi_rata2 = korelasi_rata2.round(2)

max_corr = korelasi_rata2.max()
faktor_terkuat = korelasi_rata2[korelasi_rata2 == max_corr]
faktor_str = ", ".join([f"{kol}: {nilai:.2f}" for kol, nilai in faktor_terkuat.items()])
st.metric("Faktor yang Paling Mempengaruhi Kualitas Udara", value=faktor_str)



fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(korelasi_data, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)
