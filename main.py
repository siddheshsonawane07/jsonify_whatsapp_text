import re
import json
import streamlit as st

def convert_chat_to_clean_json(chat_content):
    try:
        dateRegex = r"[\d]{1,2}/[\d]{1,2}/[\d]{2}"  
        timeRegex = r"[\d]{1,2}:\d{2}\s*(?:[aApP][mM])" 
        messageRegex = dateRegex + r', ' + timeRegex + r' - (.*?): (.*)'

        messages = []

        for line in chat_content.splitlines():
            line = line.strip()  
            message_match = re.match(messageRegex, line)
            if message_match:
                sender = message_match.group(1)
                text = message_match.group(2)
                messages.append({"sender": sender, "message": text})
             # Add to previous message if continuation
            elif messages: 
                # Handle multi-line messages
                messages[-1]["message"] += '\n' + line  

        return messages

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("WhatsApp Chat Converter")

    st.subheader("How to use this tool?")
    instructions = (
        "1. Open the WhatsApp chat you want to process.\n"
        "2. Click on the three-dot menu in the chat window.\n"
        "3. Select 'More' from the dropdown.\n"
        "4. Choose 'Export Chat' and download the .txt file.\n"
        "5. Upload the downloaded file on this website to receive the JSON-formatted output."
    )
    st.write(instructions)
    
    chat_file = st.file_uploader("Upload your WhatsApp Chat (.txt)", type=["txt"])
    
    if chat_file is not None:
        chat_content = chat_file.read().decode('utf-8')
        
        messages = convert_chat_to_clean_json(chat_content)
        
        if messages:
            st.success("Chat successfully converted!")
            
            # # Display the extracted messages
            # st.write("Extracted Messages:")
            # st.json(messages)
            
            # Option to download JSON
            json_data = json.dumps(messages, indent=3)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name='chat_clean.json',
                mime='application/json'
            )

if __name__ == '__main__':
    main()
