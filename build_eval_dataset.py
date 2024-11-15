import csv

# Dialogue data
data = [
    [
        1,
        "Get Order Status",
        "Clear status order check, Retrieve the order ID from the chat history.",
        "Bot: Welcome to BestCompany! I'm Anne, your virtual assistant. This is an open-language chat, but I can also handle some requests automatically. Common actions I can assist with include checking order status, providing return policy information, and connecting you with a human representative. How can I help you today?\
            User: Hi Anne, can you check the status of my order 1040A?\
            Bot: I understand that you want help with Check Order Status. If I'm correct, please type 'yes'. Otherwise, type 'no'.\
            User: Yes.\
            Bot: The status of your order 1040A is: On Hold. If you have any other questions, feel free to ask!\
            User: Could you tell me why it's on hold?\
            Bot: I understand that you want help with Check Order Status. If I'm correct, please type 'yes'. Otherwise, type 'no'.\
            User: No, I know the status. I'm asking why it's on hold.\
            Bot: I apologize for any frustration. Let me check why your order 1040A is on hold. Could you please provide me with your email address or phone number associated with the order? If you'd prefer, I can also connect you with a human representative to assist further.\
            User: Yes, I would prefer to speak with a human representative, please.\
            Bot: I understand that you want help with Request Human Representative. If I'm correct, please type 'yes'. Otherwise, type 'no'.\
            User: yes\
            Bot: To leave a request for a human representative, I'll need three things. First, please enter your full name:\
            User: Jane Doe\
            Bot: Great! Now, please enter your email address:\
            User: Jane@gmail.com\
            Bot: Lastly, please enter your phone number:\
            User: 0500000000\
            Bot: Your request to speak with a representative has been forwarded, and someone will get back to you shortly. Is there anything else I can assist you with in the meantime?\
            User: That's everything for now, thank you.",
    ],
    [
        2,
        "Get Order Status and if not possible, submit a request for a Human Representative",
        "Messy Checking Status Order with Complications, Recommend switching to a human representative if necessary",
        "Bot: Welcome to BestCompany! I'm Anne, your virtual assistant. This is an open-language chat, but I can also handle some requests automatically. Common actions I can assist with include checking order status, providing return policy information, and connecting you with a human representative. How can I help you today?\
        User: Hi Anne, I need to check the status of my order. It's really important.\
        Bot: I understand that you want help with Check Order Status. If I'm correct, please type 'yes'. Otherwise, type 'no'.\
        User: Yes.\
        Bot: To check your order status, I'll need the order ID. It should be four digits followed by an uppercase letter (e.g., 0000G).\
        User: I don't have my order ID with me right now, but I know the order was placed last week, if that helps.\
        Bot: No worries! I can still help you out. Could you please provide me with the email address or phone number you used to place the order? This will help me locate your order.\
        User: Sure, the email address I used is lola.m@gmail.com.\
        Bot: I understand that you want help with Check Order Status. If I'm correct, please type 'yes'. Otherwise, type 'no'.\
        User: Once again, yes.\
        Bot: To check your order status, I'll need the order ID. It should be four digits followed by an uppercase letter (e.g., 0000G).\
        User: But I don't have it! Can't you understand??\
        Bot: I'm so sorry for the inconvenience. It looks like I'm having trouble understanding your request. To assist you better, could you please provide either your email address or phone number used during the purchase? If you're still experiencing issues, I'd be happy to take your contact information for a human representative to get in touch with you.\
        User: I would like to v to resolve this issue.\
        Bot: I understand that you want help with Request Human Representative. If I'm correct, please type 'yes'. Otherwise, type 'no'.\
        User: Yes.\
        Bot: To leave a request for a human representative, I'll need three things. First, please enter your full name:\
        User: Lola Mery.\
        Bot: Great! Now, please enter your email address:\
        User: lola.m@gmail.com.\
        Bot: Lastly, please enter your phone number:\
        User: 0545465656.\
        Bot: Your request to speak with a representative has been forwarded, and someone will get back to you shortly. Is there anything else I can assist you with in the meantime?\
        User: Bye.\
        Bot: It was great talking to you. If you need anything else in the future, don't hesitate to reach out. Have a great day!",
    ],
    [
        3,
        "Submit request for human representative",
        "Request Human Representative",
        "Bot: Welcome to BestCompany! I'm Anne, your virtual assistant. This is an open-language chat, but I can also handle some requests automatically. Common actions I can assist with include checking order status, providing return policy information, and connecting you with a human representative. How can I help you today?\
        User: Hi, I want speak with human. Help now.\
        Bot: I understand that you want help with Request Human Representative. If I'm correct, please type 'yes'. Otherwise, type 'no'.\
        User: I don't know what is 'Request Human Representative'\
        Bot: I apologize for any confusion. 'Request Human Representative' means you want to speak with a human customer service agent. If you'd like, I can take your contact information and have someone reach out to you as soon as possible. How can I assist you further?\
        User: Great. Let's do it.\
        Bot: I understand that you want help with Request Human Representative. If I'm correct, please type 'yes'. Otherwise, type 'no'.\
        User: Yes.\
        Bot: To leave a request for a human representative, I'll need three things. First, please enter your full name:\
        User: Yevgeny\
        Bot: Great! Now, please enter your email address:\
        User: YeVb@gmail.com\
        Bot: Lastly, please enter your phone number:\
        User: 0562432142\
        Bot: Your request to speak with a representative has been forwarded, and someone will get back to you shortly. Is there anything else I can assist you with in the meantime?\
        User: Bye.\
        Bot: It was great talking to you. If you need anything else in the future, don't hesitate to reach out. Have a great day!",
    ],
    [
        4,
        "Get information about three aspects of the return policy: general return policy, items that cannot be returned, and how you will receive your refund.",
        "Return Policies",
        "Bot: Welcome to BestCompany! I'm Anne, your virtual assistant. This is an open-language chat, but I can also handle some requests automatically. Common actions I can assist with include checking order status, providing return policy information, and connecting you with a human representative. How can I help you today?\
        User: Hello, I'm hesitant to order a dress because I'm not sure if it will fit me. What is the return policy?\
        Bot: You can return most items within 30 days of purchase for a full refund or exchange. Items must be in their original condition, with all tags and packaging intact. Please bring your receipt or proof of purchase when returning items.\
        User: Most items? What are the exceptions?\
        Bot: Yes, certain items such as clearance merchandise, perishable goods, and personal care items are non-returnable. Please check the product description or ask a store associate for more details.\
        User: Understood, I feel more confident placing the order now.\
        Bot: I'm glad to hear that! If you have any other questions or need further assistance, feel free to reach out. Happy shopping at BestCompany!\
        User: Actually I also wanted to know what the return policy is.\
        Bot: You can return most items within 30 days of purchase for a full refund or exchange. Items must be in their original condition, with all tags and packaging intact. Please bring your receipt or proof of purchase when returning items.\
        User: Thank you. Bye.\
        Bot: It was great talking to you. If you need anything else in the future, don't hesitate to reach out. Have a great day!",
    ],

]

# Specify the file name
file_name = 'predefined_dialogues.csv'

# Column headers for the CSV file
headers = ['Dialogue ID', 'Task', 'Scenario','Dialogue']

# Writing to a CSV file
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)

print("Data successfully written to", file_name)


