from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import streamlit as st
import pandas as pd
from data_cleaning import clean_data
# initial_df = None

@st.cache_data
def web_scraping(url):
  options = webdriver.ChromeOptions()
  options.add_argument("--headless=new")
  options.add_argument(f'--user-agent={"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}')
  options.add_argument("start-maximized")
  driver = webdriver.Chrome(options=options)
  driver.get(url)
  time.sleep(5)
  final_result = []
  index = 0

  while True:
    bus_elements = driver.find_elements(By.CLASS_NAME, "bus-item-details")
    if len(bus_elements) ==  index+1:
      break
    else:
      elements = bus_elements[index]
      index+=1
      driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", elements)
      time.sleep(2)
      try:
        bus_name = elements.find_element(By.CLASS_NAME, "travels").text
      except:
        bus_name = "no data"
      try:
        start_location = elements.find_element(By.CLASS_NAME, "bp-loc").text
      except: 
        bus_name = "no data"
      try:
        end_location = elements.find_element(By.CLASS_NAME, "bp-loc").text
      except: 
        bus_name = "no data"
      try:
        bus_type = elements.find_element(By.CLASS_NAME, "bus-type").text
      except: 
        bus_name = "no data"
      try:
        duration = elements.find_element(By.CLASS_NAME, "dur").text
      except: 
        bus_name = "no data"
      try:
        departure_time = elements.find_element(By.CLASS_NAME, "dp-time").text
      except: 
        bus_name = "no data"
      try:
        reaching_time = elements.find_element(By.CLASS_NAME, "bp-time").text
      except:  
        bus_name = "no data"
      try:
        star_rating = elements.find_element(By.CLASS_NAME, "rating-sec").text
      except:  
        bus_name = "no data"
      try:
        price = elements.find_element(By.CLASS_NAME, "fare").text
      except:  
        bus_name = "no data"
      try:
        seat_availability = elements.find_element(By.CLASS_NAME, "seat-left").text
      except:  
        bus_name = "no data"
      data = {"Bus Name" : bus_name, "Start Location" : start_location, "End Location" : end_location, "Bus Type" : bus_type, "Travel Duration" : duration, "Departure Time" : departure_time, "Reaching Time" : reaching_time, "Star Rating" : star_rating, "Price" : price, "Seat Availability" : seat_availability}
      final_result.append(data)
  driver.quit()
  
  return final_result

###########################################################################################
def main():
    st.title('Bus Service Finder')
    
    url = st.text_input("Please enter a redbus URL:")
    if url:
        if 'scraped_data' not in st.session_state or st.session_state['url'] != url:
            with st.spinner("Collecting data from the link provided. Please wait..."):
                st.session_state['scraped_data'] = web_scraping(url)
                st.session_state['url'] = url
        
        final_result = st.session_state['scraped_data']
        df = pd.DataFrame(final_result)
        df = clean_data(df)
        
        st.sidebar.header("Filter Options")
        star_rating = st.sidebar.slider('Select Star Rating', min_value=1.0, max_value=5.0, value=(1.0, 5.0), step=0.1)
        price_range = st.sidebar.slider(
            'Select Price Range',
            min_value=int(df['Price'].min()), 
            max_value=int(df['Price'].max()), 
            value=(int(df['Price'].min()), int(df['Price'].max()))
        )
        
        with st.spinner("Filtering data based on your selections. Please wait..."):
            filtered_df = df[
                (df['Star Rating'] >= star_rating[0]) &
                (df['Star Rating'] <= star_rating[1]) &
                (df['Price'] >= price_range[0]) &
                (df['Price'] <= price_range[1])
            ]
        
        st.title("Redbus Data Filtering")
        st.write("Apply filters using the sidebar to narrow down your results.")
        st.write(f"Displaying {len(filtered_df)} buses out of {len(df)}:")
        st.dataframe(filtered_df)
###########################################################################################
# def main():
#     st.title('Bus Service Finder')
#     # Prompt the user to enter a URL
#     url = st.text_input("Please enter a redbus URL:")
#     if url:
#         with st.spinner("Collecting data from the link provided. Please wait..."):
#             final_result = web_scraping(url)
#         df = pd.DataFrame(final_result)
#         df = clean_data(df)
#         # Sidebar Filters
#         st.sidebar.header("Filter Options")
#         star_rating = st.sidebar.slider('Select Star Rating', min_value=1.0, max_value=5.0, value=(1.0, 5.0), step=0.1)
#         # Add other filters if needed (e.g., price range, seat availability)
#         price_range = st.sidebar.slider('Select Price Range', min_value=int(df['Price'].min()), max_value=int(df['Price'].max()), value=(int(df['Price'].min()), int(df['Price'].max())))
#         # Store the initial DataFrame so we don't scrape again
#         initial_df = df
#         # Filtering already collected data
#         with st.spinner("Filtering data based on your selections. Please wait..."):
#             filtered_df = initial_df[(initial_df['Star Rating'] >= star_rating[0]) & (initial_df['Star Rating'] <= star_rating[1]) & (initial_df['Price'] >= price_range[0]) & (initial_df['Price'] <= price_range[1])]
#         # Main Application
#         st.title("Redbus Data Filtering")
#         st.write("Apply filters using the sidebar to narrow down your results.")
#         st.write(f"Displaying {len(filtered_df)} buses out of {len(initial_df)}:")
#         st.dataframe(filtered_df)

if __name__ == "__main__":
  main()