import streamlit as st
from vitcevents import VITCEvents
from devfolio import Devfolio
import asyncio
import json

shown=False

# Create a form
with st.form(key='registration_form'):
    # Create form fields
    option = st.selectbox(
    'What Sites do you want to be displayed',
    ('VIT Chennai Events', 'Devfolio'))
  
    fee=st.text_input(label='Max Event fee')
     # Create a submit button
    submitted = st.form_submit_button(label='Show Events')

    # Display a success message when the form is submitted
    if submitted:
        st.success(f'Showing events for your price from {option}!')
        # st.balloons()
    if option=='VIT Chennai Events':
        scrape=VITCEvents()
        data=asyncio.run(scrape.push_all_cards(write=False))
        for item in data:
            try:
                if(int(item['fee'])<=int(fee)):
                    shown=True
                    st.subheader(f" :blue[{item['eventname']}] :sunglasses:")
                    st.write(f"Given event desciption --> {item['eventdesc']}")
                    st.write(f"Event fees is {item['fee']}")
                    if(item['venue']== 'VIT Chennai'):
                        st.write(f"Offline event")
                    else:
                        st.write(f"Online event")
                    st.write(f"Event date is {item['eventdate']}")
            except ValueError:
                st.write("Please enter an amount to display events in the range")
                break
        if(not shown and submitted):
            st.write("No events found for your price")
            # st.write(json.dumps(item, indent=4))

    elif option=='Devfolio':
        scrapedev=Devfolio()
        data=scrapedev.findall()
        for item in data:
            try:
                shown=True
                st.subheader(f":blue[{item['_source']['name']}]")
                st.write(f"Given event desciption --> {item['_source']['tagline']}")
                # st.write(f"Event fees is {item['_source']['fee']}")
                if(item['_source']['is_online']== 'true'):
                    st.write(f"Online event")
                else:
                    st.write(f"Location is {item['_source']['location']}")
                st.write(f"Event date is {scrapedev._getdatetime_(item['_source']['starts_at'],item['_source']['ends_at'])}")
                
            except ValueError:
                st.write("Please enter an amount to display events in the range")
                break