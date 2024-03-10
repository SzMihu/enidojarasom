from urllib.request import urlopen
from bs4 import BeautifulSoup
import streamlit as st

page_bg_img = f'''
<style>
.stApp {{
background-image: url("https://media.istockphoto.com/id/1157569060/hu/fot%C3%B3/gy%C3%B6ny%C3%B6r%C5%B1-tiszta-k%C3%A9k-%C3%A9g-h%C3%A1tt%C3%A9r-sima-nagy-feh%C3%A9r-felh%C5%91-a-reggeli-id%C5%91sugarak-napf%C3%A9ny-sz%C3%B3k%C3%B6zt-a.jpg?s=1024x1024&w=is&k=20&c=uOvofqjcjrtORw5MwbooayNGxdf5jFk4TUZUpMwUwuQ=");
background-size: cover;
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

selectors = ["body > app-root > app-base > div.content-wrap > app-text-forecast > section > div > div > koponyeg-text-forecasts > div.text-forecasts > koponyeg-text-forecast-card:nth-child(1) > div.text-forecast-day",
             "body > app-root > app-base > div.content-wrap > app-text-forecast > section > div > div > koponyeg-text-forecasts > div.text-forecasts > koponyeg-text-forecast-card:nth-child(1) > div.text-forecast-description",
             "body > app-root > app-base > div.content-wrap > app-text-forecast > section > div > div > koponyeg-text-forecasts > div.text-forecasts > koponyeg-text-forecast-card:nth-child(2) > div.text-forecast-day",
             "body > app-root > app-base > div.content-wrap > app-text-forecast > section > div > div > koponyeg-text-forecasts > div.text-forecasts > koponyeg-text-forecast-card:nth-child(2) > div.text-forecast-description",
             "body > app-root > app-base > div.content-wrap > app-text-forecast > section > div > div > koponyeg-text-forecasts > div.text-forecasts > koponyeg-text-forecast-card:nth-child(3) > div.text-forecast-day",
             "body > app-root > app-base > div.content-wrap > app-text-forecast > section > div > div > koponyeg-text-forecasts > div.text-forecasts > koponyeg-text-forecast-card:nth-child(3) > div.text-forecast-description"]

url = "https://koponyeg.hu/elorejelzes/szoveges"

html = urlopen(url)
soup = BeautifulSoup(html, features="html.parser")

st.subheader("Szöveges előrejelzés (Budapest)")

for i in range(len(selectors)):
    szoveg = soup.select(selectors[i])
    cleantext = BeautifulSoup(str(szoveg), "html.parser").get_text()
    onlytext = cleantext.strip("[]")

    st.write(onlytext)