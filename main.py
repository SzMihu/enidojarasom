import requests
import streamlit as st
import time
import pandas




API_KEY = st.text_input("API kulcs openweathermap.org oldalhoz", type="password")

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
    firstday = dayly_data[:8]
    temperature = [dict["main"]["temp"] for dict in firstday]
    hours = [h["dt_txt"][11:16] for h in firstday]
    icons = [i["weather"][0]["icon"] for i in firstday]
    descriptions = [i["weather"][0]["description"] for i in firstday]
    now = time.strftime("%H:%M")
    maxok = []
    minek = []
    napok = []
    desc1 = []
    desc2 = []
    for i in dayly_data:
        if i["dt_txt"][11:13] == "12":
            maxok.append(i["main"]["temp_max"])
            napok.append(i["dt_txt"][5:10])
            desc1.append(i["weather"][0]["description"])
    for i in dayly_data:
        if i["dt_txt"][11:13] == "00":
            minek.append(i["main"]["temp_min"])
            desc2.append(i["weather"][0]["description"])

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            temp = firstdata["main"]["temp"]
            st.title(now)
            st.title(f'{int(temp)} °C')
            g = st.toggle("mutass valamit")
            if g:
                st.info("nagy siker")

        with col2:
            sky = firstdata["weather"][0]["icon"]
            st.subheader(firstdata["weather"][0]["description"])
            st.image(f"images/{sky}@2x.png", width=220)

        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
        cols = [c1, c2, c3, c4, c5, c6, c7, c8]
        ind = 0
        for i in cols:
            with i:
                i.subheader(hours[ind])
                i.subheader(f"{int(temperature[ind])} °C")
                i.image(f"images/{icons[ind]}@2x.png", width=70)
                i.write(descriptions[ind])

                ind = ind + 1

        gomb = st.button("nyomd meg")
        if gomb:
            st.balloons()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([f"{napok[0]}", f"{napok[1]}", f"{napok[2]}",
                                            f"{napok[3]}", f"{napok[4]}"])
    tabs = [tab1, tab2, tab3, tab4, tab5]
    szam = 0
    for tetel in tabs:
        with tetel:
            st.write(f"nappal {int(maxok[szam])}°C, {desc1[szam]}")
            st.write(f"éjjel {int(minek[szam])}°C, {desc2[szam]}")
        szam += 1

    chart_data = pandas.DataFrame({"hőfok":[dict["main"]["temp"] for dict in dayly_data],
                "dátum":[dict["dt_txt"] for dict in dayly_data]})
    st.subheader("Hőmérsékletváltozás")
    st.bar_chart(chart_data, x="dátum", y="hőfok", color=[0.0, 1.0, 0.0])