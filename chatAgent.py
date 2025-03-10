import streamlit as st
import requests
import json
from streamlit.logger import get_logger
from streamlit_js_eval import streamlit_js_eval

LOGGER = get_logger(__name__)

API_URL = "https://documentchatbot-production.up.railway.app/chat"

def is_dark_mode():
    is_dark_mode = streamlit_js_eval(js_expressions="window.matchMedia('(prefers-color-scheme: dark)').matches", key="theme")

    if is_dark_mode:        
        avatar_url = "./white_bruin.png"         
    else:                
        avatar_url = "./bruin.png"  

    return avatar_url    

def main():       

    avatar_url = is_dark_mode()     
        
    st.title("Handbook Chatbot")
    
    st.sidebar.title("About")
    st.sidebar.html(
        """
        Looking for informaiton from the <a href="https://www.bps-ok.org/documents/parents-%26-students/student-handbooks/359802" target="_blank">Bartlesville High School</a> handbook? 
        <br><br>
        This friendly chatbot is here to help by providing answers straight from the official handbook.
        <br><br>
        <a href="https://blog.paulmrichardson.com/handbook-chatbot-change-log" target="_blank">More Information & Change Log...</a>"""
    )
    
    st.sidebar.info(        
        """
        Developed by: Paul Richardson 
    """)

    st.sidebar.title("Disclaimer") 
    st.sidebar.html("""
        This chatbot is an independent learning project developed solely for educational purposes. 
        It is not an official resource of Bartlesville High School or any Bartlesville Public School entity. 
        While responses are generated from the Bartlesville High School Student Handbook, the accuracy,
        completeness, or currency of information provided cannot be guaranteed. 
        Users should always <b>VERIFY INFORMATION DIRECTLY WITH OFFICIAL SCHOOL RESOURCES</b> before making 
        decisions or taking action based on the chatbot’s responses. 
        <br><br>
        This tool is hosted using free and open-source resources; therefore, availability, performance, and response times may vary.
          
    """)
   

     # Initialize session state for chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar", None)):
            st.markdown(message["content"])
         
        
    # Default model choice  
    model_choice = "llama"   

    # Display initial message
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar=avatar_url):
            initial_message = "Hello! I am your Bartlesville High School Handbook assistant. How can I help you today?"
            st.markdown(initial_message)
            st.session_state.messages.append({"role": "assistant", "content": initial_message, "avatar": avatar_url})            

    # User input    
    if user_query := st.chat_input("Ask a question:"):
        response, error = send_query(user_query, model_choice)

        if error:
            #st.error(f"Error in getting response from the API: {error}")
            
            with st.chat_message("assistant", avatar= avatar_url):
                st.markdown(f"{response.get('detail', 'No response from the API.')}\n")                
                st.session_state.messages.append({"role": "assistant", "content": response.get('detail', 'No reponse from API'), "avatar": avatar_url})                
        else:
            if response:                            
                with st.chat_message("user"):
                    st.markdown(f"{user_query}")
                    st.session_state.messages.append({"role": "user", "content": user_query})                
                with st.chat_message("assistant", avatar= avatar_url):
                    st.markdown(f"{response.get('result', 'No response from the API.')}\n")                
                    st.session_state.messages.append({"role": "assistant", "content": response.get('result', 'No reponse from API'), "avatar": avatar_url})
            else:
                st.error("Error in getting response from the API.")
    
def send_query(query, model):
    payload = {
        "query": query,
        "model": model
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()        
        return response.json(), None
    except requests.exceptions.RequestException as e:        
        return response.json(), str(e)    

def fake_query(query, model):
    # Simulate a hardcoded JSON response
    response = {
        "query": query,
        "result": "<think>\nOkay, so I need to figure out what's considered an excused absence according to the Bartlesville High School handbook. Let me start by looking through the content provided. \n\nFirst, I remember seeing a section about absentee codes. It lists two categories: those that count against exemptions and those that don't. The ones that don't count against exemptions are probably the excused ones. \n\nLooking at the codes that don't count against exemptions, they include Act (School Activity), Ofc (in office), Cns (with counselor), Nrs (with Nurse), Tch (with Teacher), Fnl (Absence for Funeral), BOT/PASS (In school Suspension), and Crt (Absence for Court). \n\nWait, but the user is asking about excused absences, not just those that don't count against exemptions. I should make sure these are the same thing. The handbook mentions exemptions, which I think are related to being excused from finals. So, these codes likely represent excused absences. \n\nAdditionally, there's a section about make-up work that says absences can be excused, and students have two days to make up work per day missed. It also mentions that excused absences include things like funerals and religious observances, as seen in points 5 and 6 of the context. \n\nSo, putting it all together, excused absences are those with the codes Act, Ofc, Cns, Nrs, Tch, Fnl, BOT/PASS, and Crt. Also, attending funerals or religious observances are excused. \n\nI should structure the answer to list these codes and their meanings, citing the relevant sections. Since the exact page number isn't clear, I'll mention the section on Absentee Codes and the make-up work section.\n</think>\n\nAccording to the Bartlesville High School handbook, excused absences are those that do not count against exemptions. These include:\n\n- Act: School Activity\n- Ofc: In office\n- Cns: With counselor\n- Nrs: With Nurse\n- Tch: With Teacher\n- Fnl: Absence for Funeral\n- BOT/PASS: In school Suspension\n- Crt: Absence for Court\n\nAdditionally, attending funerals or observing religious holidays are considered excused absences. \n\nThese details can be found in the sections on Absentee Codes and Make-Up Work for Absences. \n\nIf you need further clarification, please refer to the relevant sections or contact the school directly."
    }
    return response    


if __name__ == "__main__":
    main()
