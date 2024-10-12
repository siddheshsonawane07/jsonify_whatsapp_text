import re
import json
import streamlit as st
from collections import defaultdict

def parse_and_convert_chat(chat_content):
    try:
        dateRegex = r"[\d]{1,2}/[\d]{1,2}/[\d]{2}"  
        timeRegex = r"[\d]{1,2}:\d{2}\s*(?:[aApP][mM])" 
        messageRegex = dateRegex + r', ' + timeRegex + r' - (.*?): (.*)'

        messages_by_sender = defaultdict(list)
        complete_chat = []

        for line in chat_content.splitlines():
            line = line.strip()
            message_match = re.match(messageRegex, line)
            if message_match:
                sender = message_match.group(1)
                text = message_match.group(2)

                # Append to individual sender's list
                messages_by_sender[sender].append({"message": text})

                # Append to complete chat
                complete_chat.append({"sender": sender, "message": text})
            
            elif complete_chat:
                # Handle multi-line messages
                last_sender = list(messages_by_sender.keys())[-1]
                messages_by_sender[last_sender][-1]["message"] += '\n' + line
                complete_chat[-1]["message"] += '\n' + line

        return dict(messages_by_sender), complete_chat

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

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
        
        messages_by_sender, complete_chat = parse_and_convert_chat(chat_content)
        
        if messages_by_sender and complete_chat:
            st.success("Chat successfully converted!")
            
            # Option to download JSON for each sender
            for sender, messages in messages_by_sender.items():
                json_data = json.dumps(messages, indent=3)
                st.download_button(
                    label=f"Download JSON for {sender}",
                    data=json_data,
                    file_name=f'{sender.replace(" ", "_")}_chat.json',
                    mime='application/json'
                )

            # Option to download the complete chat
            complete_chat_json = json.dumps(complete_chat, indent=3)
            st.download_button(
                label="Download Complete Chat",
                data=complete_chat_json,
                file_name='complete_chat.json',
                mime='application/json'
            )

if __name__ == '__main__':
    main()
