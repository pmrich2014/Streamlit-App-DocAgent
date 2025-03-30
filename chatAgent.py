import streamlit as st
import requests
from requests.models import Response
import json
from streamlit.logger import get_logger
from streamlit_js_eval import streamlit_js_eval
from better_profanity import profanity  
# from dotenv import load_dotenv
import os

#load_dotenv()

# API_KEY_APP = os.getenv("API_KEY_APP")
# API_URL = os.getenv("API_URL")

LOGGER = get_logger(__name__)

 # Update with the correct API URL if needed

def is_dark_mode():
    is_dark_mode = streamlit_js_eval(js_expressions="window.matchMedia('(prefers-color-scheme: dark)').matches", key="theme")

    if is_dark_mode:        
        avatar_url = "bruin_white.png"          
    else:               
        avatar_url = "bruin.png"  

    return avatar_url    


def main():       

    avatar_url = is_dark_mode()
    # print(avatar_url)   
        
    st.title("Handbook Chatbot")
    
    st.sidebar.title("About")
    st.sidebar.html(
        """
        This friendly chatbot is here to help by providing answers from the BHS handbook and event calendar.
        <br><br>
        <a href="https://blog.paulmrichardson.com/handbook-chatbot-change-log" target="_blank">More Information & Change Log...</a>
        <br><br>
        Answers are sourced from the following documents:
        <ul><a href="https://www.bps-ok.org/documents/parents-%26-students/student-handbooks/359802" target="_blank">Bartlesville High School Handbook</a>
        <ul><a href="https://calendar.google.com/calendar/u/0/embed?src=bps-ok.org_k9egfkkhgo7p8auk5stmq654ng@group.calendar.google.com&ctz=America/Chicago" target="_blank">BHS Google Event Calendar</a>
       """
    )
    
    st.sidebar.info(        
        """
        Developed by: Paul Richardson 
    """)

    st.sidebar.title("Disclaimer") 
    st.sidebar.html("""
        This chatbot is an independent learning project developed solely for educational purposes. 
        It is not an official resource of Bartlesville High School or any Bartlesville Public School entity. 
        While responses are generated from the Bartlesville High School resources, the accuracy,
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

    #greeting = "Hello! I am your Bartlesville High School assistant. \n\n I can help answer questions directly from the  \
    #            Bartlesville High School (BHS) Student Handbook. Or I can answer questions from BHS event calendar for upcoming events. \
    #            To get started, simply ask me a question. For example, you can ask about the dress code policy, graduation elgibilty, or about  \
    #            upcoming events I can help! If you have a question, please ask and I will do my best to provide an answer. " 
    
    greeting = greeting = """
                            👋 I'm your friendly **Bartlesville High School assistant**! I can help you:

                            - 📚 **Answer questions** from the BHS Student Handbook
                            - 📆 **Provide information** about upcoming BHS events from the BHS event calendar

                            To get started, just type a question. For example:

                            - *What’s the dress code policy?*                            
                            - *What if a student becomes iss or is injured at school?*
                            - *What if a student needs to take medication during school hours?*
                            - *What's happening at BHS this week?*
                            - *What is the last day of school?*

                            I'm here and ready to help!
                            """
    # Display initial message
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar=avatar_url):
            initial_message = greeting
            st.markdown(initial_message)
            st.session_state.messages.append({"role": "assistant", "content": initial_message, "avatar": avatar_url})            

    # User input    
    if user_query := st.chat_input("Ask a question:"):

        # Check for profanity
        if profanity.contains_profanity(user_query):
            st.error("Profanity is not allowed. Please rephrase your question.")
            return
        
        response, error = send_query(user_query)

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
                    st.markdown(f"{response.get('generation', 'No response from the API.')}\n")                
                    st.session_state.messages.append({"role": "assistant", "content": response.get('generation', 'No reponse from API'), "avatar": avatar_url})
            else:
                st.error("Error in getting response from the API.")
    
def send_query(query):
    
    payload = {
        "query": query                
    }

    headers = {
            "X-API-Key": API_KEY_APP
        }
    
    try:
        
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()        
        print(response.json())
        return response.json(), None
    except requests.exceptions.RequestException as e:        
        return response.json(), str(e)    

def fake_query(query):
    # Simulate a hardcoded JSON response
    
    response = {'question': 'What are the dress code policies outlined in the school handbook?', 'generation': 'According to the Bartlesville High School Handbook, the dress code policies are as follows: \n\n* Caps, hats, bandanas, or other head coverings may be worn in the school building when previously approved by the school’s administration for medical or religious reasons or for a school activity (Section on Apparel for the Head or Face).\n* Sunglasses, unless prescribed by a physician to wear in the classroom, shall not be worn to class (Section on Apparel for the Head or Face).\n* Sleeveless shirts or blouses may be worn provided that the arm opening is not unnecessarily revealing of the student’s body or undergarments (Section on Upper Garments).\n* Tank tops, spaghetti tops, and basketball jerseys are permitted only when worn in combination with another shirt such that the combination meets the original dress code (Section on Upper Garments).\n* It is not permitted to wear clothing that exposes the back and/or shoulders. Immodestly low necklines, and/or bare midriffs are prohibited (Section on Upper Garments).\n* Pants and shorts shall be worn at the waist. Undergarments shall not be visible (Section on Lower Garments).\n* Tights or leggings may be worn as outerwear when worn with an appropriate upper garment (Section on Lower Garments).\n* Shorts, skirts, and dresses must be at or below the level of the fingertips or no shorter than six inches above the middle of the knee, whichever is longer (Section on Lower Garments).\n* The following decorations and/or designs imprinted upon clothing or attached to the body (temporary or permanent) are prohibited: \n  - Advertisement of tobacco, alcohol, or illegal drugs\n  - Sexually suggestive messages\n  - Vulgar or profane messages\n  - Messages advocating violence (Section on General Rules).\n* Thick metal chains, dog collars, choke chains, wallet chains, etc. are prohibited (Section on General Rules).\n* Administrators have the authority to rule on appropriateness of dress and in determining whether something might be a potential distraction from learning (Section on School Administrators or designee).\n\nThese policies are outlined in the handbook to ensure a safe and respectful learning environment for all students.', 'is_event': 'no', 'documents': [{'id': '244c7eed-35e4-4182-bb89-dde52323b308', 'metadata': {}, 'page_content': 'DRESS CODE', 'type': 'Document'}, {'id': 'cad3ff78-32d3-44cb-84fa-eadc4cbeec6e', 'metadata': {}, 'page_content': '**Apparel for the Head or Face**\n\nCaps, hats, bandanas, or other head coverings may be worn in the school building when previously approved by the school’s administration for medical or religious reasons or for a school activity.\n\nSunglasses, unless prescribed by a physician to wear in the classroom, shall not be worn to class.\n\n# **Upper Garments**\n\nSleeveless shirts or blouses may be worn provided that the arm opening is not unnecessarily revealing of the student’s body or undergarments.  The fabric is to cover the student’s shoulder from the base of the neck to the top edge of the shoulder or arm.    \nTank tops, spaghetti tops and basketball jerseys are permitted only when worn in combination with another shirt such that the combination meets the original dress code.\n\nIt is not permitted to wear clothing that exposes the back and/or shoulders.  Immodestly low necklines, and/or bare midriffs are prohibited.  Garments must be of appropriate length and fit to meet these requirements while sitting and/or bending.\n\n# **Lower Garments**\n\nPants and shorts shall be worn at the waist.  Undergarments shall not be visible.  \nTights or leggings may be worn as outerwear when worn with an appropriate upper garment.  \nShorts, skirts, and dresses must be at or below the level of the fingertips or no shorter than\xa0six inches above the middle of the\xa0knee, whichever is longer. Administrators have the authority to rule on appropriateness.', 'type': 'Document'}, {'id': '7d884c1a-82b9-4678-9d4f-69935cf40b63', 'metadata': {}, 'page_content': '**General Rules**\n\nThe following decorations and/or designs imprinted upon clothing or attached to the body (temporary or permanent) are prohibited:\n\n•\tAdvertisement of tobacco, alcohol, or illegal drugs\n\n•\tSexually suggestive messages\n\n•\tVulgar or profane messages\n\n•\tMessages advocating violence\n\nAll students participating in approved school activities are expected to comply with required dress code regulations while in class. Students who participate in school sponsored extracurricular activities must have their uniforms approved by the secondary school administration.  Spirit squads may be allowed to wear uniforms as approved by the building administration.\n\nThick metal chains, dog collars, choke chains, wallet chains, etc. are prohibited.', 'type': 'Document'}, {'id': '27197784-2726-4001-bc68-34c4a27b62b8', 'metadata': {}, 'page_content': '**Consequences/Penalties**\n\nStudents who elect not to conform to the dress code set forth by this policy will be subject to disciplinary action.', 'type': 'Document'}, {'id': '3916e415-8acf-495b-bd42-618ef571d95e', 'metadata': {}, 'page_content': '**School Administrators or designee shall have the authority to rule on appropriateness of dress and in determining whether something might be a potential distraction from learning.**', 'type': 'Document'}, {'id': '4ce3a7e0-89dc-4791-ae7a-f411634618a1', 'metadata': {}, 'page_content': '**Grievance Policy, Procedure and Form**\n\nEmployees, students and other individuals are to conduct themselves so that students may attend school in an educational environment free from discrimination or harassment on the basis of race, color, national origin, sex, religion, age or disability.\n\nThe district strictly prohibits all forms of discrimination or harassment on school grounds, in school vehicles, and at all school-sponsored activities, programs and events, including school events that take place at locations outside the district. The district also strictly prohibits all forms of discrimination or harassment against individuals associated with the district.\n\nIt is a violation of Board Policy FAA for any student, employee or third-party, such as school visitors and vendors, etc., to subject any student, employee, or any other individual to discrimination or harassment.\n\nThe district encourages students and employees who feel they have been subjected to  \ndiscrimination or harassment, and persons with knowledge of discrimination or  \nharassment, to report such immediately. All complainants have the right to be free from  \nretaliation for filing a complaint.\n\nMore information regarding Board Policy FAA, Harassment and Discrimination may be found on the district’s website under Board Policies.', 'type': 'Document'}, {'id': '6a1659d7-715b-4f18-930b-b471c258074c', 'metadata': {}, 'page_content': 'ACCOUNTABILITY STATEMENT\n\nAs a student in the Bartlesville Public Schools, it is my responsibility to:\n\n•\tattend school regularly and be on time to class;\n\n•\tunderstand and obey class and school rules;\n\n•\tcome to school properly prepared with materials, assignments, and a positive frame of mind;\n\n•\tseek answers to questions and participate in class until I understand;\n\n•\ttake ownership of my learning, believe in my abilities and have high expectations for myself in my class work, homework, assessments and citizenship; and,\n\n•\taccept consequences for the choices I make.', 'type': 'Document'}, {'id': '9eec0f52-b62c-4905-b575-c9994c62a245', 'metadata': {}, 'page_content': 'Safe Call Hotline\t31  \nCyber Bullying and Internet Safety\t31  \nSkate Boards\t32  \nVisitors\t32  \nCounselors\t32  \nSchool Closing Due to Weather\t33  \nHall Passes\t33  \nLibraries\t33  \nLockers\t33  \nLost and Found\t33  \nFees, Fines, and Charges\t33  \nStudent Vehicle Use and Parking\t34  \nParking Permit\t34  \nPublic Display of Affection\t34  \nStudent Messages\t34  \nParent Support Group\t35  \nImmunizations\t35  \nMedication Dispensed at School\t35  \nIllness and Accidents at School\t36  \nMeningococcal Disease and Meningitis\t36  \nUpdated Asthma Health Plan\t37  \nAsbestos Notice Page\t38', 'type': 'Document'}, {'id': '1e3c0084-32f4-46e2-b731-dcd686d9d432', 'metadata': {}, 'page_content': 'STUDENT DISCIPLINE (REGULATION)\n\nIn accordance with the policy of the board of education, the following regulations shall govern student discipline.\n\nA student who violates a policy, rule or regulation shall be subject to appropriate remedial or corrective action.  The following are guidelines for some alternatives:', 'type': 'Document'}, {'id': '81f318f5-67cb-40af-b292-3d6149d51985', 'metadata': {}, 'page_content': '**MEDICATION DISPENSED IN SCHOOL**\n\n1\\.\tNon-prescription and prescription medicine may be administered at school.  Prescription medicine to be given must be in the prescription bottle with the student’s name, name of medicine, dosage, and instructions.  Non-prescription medicines must be in their original containers with the student’s name on them.\n\n2\\.\tThe parent or guardian must complete Board Policy Form, MEDICATION:  ADMINISTERING TO STUDENTS (available in school offices), giving permission to administer both prescription and non-prescription medicine each year.  All medications and authorization forms are to be taken to the student’s designated grade level office.   All other medications shall be confiscated by school authorities and released only to the parents, legal guardian, or other authority.\n\n3\\.\tAt the end of each school year, all medicine should be picked up by the parent or student.  All medicine left at school will be destroyed.', 'type': 'Document'}]}
    response = json.loads(json.dumps(response))
    return response, None 

if __name__ == "__main__":            
    main()
