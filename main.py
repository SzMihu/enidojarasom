
import requests
import streamlit as st
import time
import pandas



page_bg_img = f'''
<style>
.stApp {{
background-image: url("https://media.istockphoto.com/id/1157569060/hu/fot%C3%B3/gy%C3%B6ny%C3%B6r%C5%B1-tiszta-k%C3%A9k-%C3%A9g-h%C3%A1tt%C3%A9r-sima-nagy-feh%C3%A9r-felh%C5%91-a-reggeli-id%C5%91sugarak-napf%C3%A9ny-sz%C3%B3k%C3%B6zt-a.jpg?s=1024x1024&w=is&k=20&c=uOvofqjcjrtORw5MwbooayNGxdf5jFk4TUZUpMwUwuQ=");
background-size: cover;
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

API_KEY = st.secrets["API_KEY"]


if API_KEY:
    place = st.text_input("Válassz helyet", "Budapest")

    days = 5
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}&units=metric&lang=hu"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]
    nr_of_data = 8 * days
    dayly_data = filtered_data[:nr_of_data]
    firstdata = dayly_data[0]
    day1 = dayly_data[:8]
    day2 = dayly_data[8:16]
    day3 = dayly_data[16:24]
    day4 = dayly_data[24:32]
    day5 = dayly_data[32:40]
    temperature = [dict["main"]["temp"] for dict in day1]
    firstday = [h["dt_txt"][5:10] for h in day1]
    hours = [h["dt_txt"][11:16] for h in day1]
    icons = [i["weather"][0]["icon"] for i in day1]
    descriptions = [i["weather"][0]["description"] for i in day1]
    ws = [w["wind"]["speed"] for w in day1]
    now = time.strftime("%H:%M")
    napok = []

    for i in dayly_data:
        napok.append(i["dt_txt"][5:10])

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            temp = firstdata["main"]["temp"]
            st.title(now)
            st.title(f'{int(temp)} °C')


        with col2:
            sky = firstdata["weather"][0]["icon"]
            st.subheader("")
            st.subheader(firstdata["weather"][0]["description"])
            st.subheader(f'szél: {int(firstdata["wind"]["speed"])} km/h')

        with col3:
            st.image(f"images/{sky}@2x.png", width=220)


        gomb = st.button("nyomd meg")
        if gomb:
            st.balloons()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([f"{napok[0]}", f"{napok[7]}", f"{napok[15]}",
                                            f"{napok[23]}", f"{napok[31]}"])
    tabs = [tab1, tab2, tab3, tab4, tab5]
    days = [day1, day2, day3, day4, day5]
    szam = 0

    for item in tabs:
        with item:
            temperature = [dict["main"]["temp"] for dict in days[szam]]
            feels = [dict["main"]["feels_like"] for dict in days[szam]]
            thisdays = [h["dt_txt"][5:10] for h in days[szam]]
            hours = [h["dt_txt"][11:16] for h in days[szam]]
            icons = [i["weather"][0]["icon"] for i in days[szam]]
            descriptions = [i["weather"][0]["description"] for i in days[szam]]
            winds = [wind["wind"]["speed"] for wind in days[szam]]
            chdt = pandas.DataFrame({"hőfok": temperature, "időpont": hours, "hőérzet": feels})

            c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
            cols = [c1, c2, c3, c4, c5, c6, c7, c8]
            index = 0
            for i in cols:
                with i:
                    i.write(thisdays[index])
                    i.write(hours[index])
                    i.write(f"{int(temperature[index])} °C")
                    i.image(f"images/{icons[index]}@2x.png", width=70)
                    i.write(descriptions[index])
                    i.write(f"szél: {int(winds[index])} km/h")
                    index = index + 1
            szam = szam + 1

            st.write("napi hőmérséklet")
            st.line_chart(chdt, x="időpont", y=["hőfok", "hőérzet"], color=[[0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

    chart_data = pandas.DataFrame({"hőfok": [dict["main"]["temp"] for dict in dayly_data],
                                   "dátum": [dict["dt_txt"] for dict in dayly_data]})
    st.subheader("Hőmérsékletváltozás 5 napra")
    st.bar_chart(chart_data, x="dátum", y="hőfok", color=[0.0, 1.0, 0.0])