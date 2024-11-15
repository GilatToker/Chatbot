import os
import re
import pandas as pd
from flask import Flask, render_template, request
from openai import OpenAI
import csv
import datetime

app = Flask(__name__)

# Set up Gpt
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

def api_function(prompt):
    """
       Interact with the OpenAI API to get a response based on the provided prompt.

       Args:
           prompt (list): A list of dictionaries representing the conversation history
                          and the current user input. Each dictionary contains a 'role'
                          and 'content' key.

       Returns:
           str: The generated response text from the OpenAI API, or an error message
                if an exception occurs.
       """

    try:
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=prompt,
            temperature=0.7,
            max_tokens=100,
        )
        # Extract the generated text from the API response
        generated_text = response.choices[0].message.content if hasattr(response.choices[0].message,
                                                                        'content') else ''
        return generated_text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_order_status(order_id):
    """
       Retrieve the status of an order given its ID.

       Args:
           order_id (str): The ID of the order to check the status for.

       Returns:
           str: The status of the order if found, or a message indicating the order ID was not found.
       """

    # Load the orders data from the CSV file
    orders_df = pd.read_csv('Orders.csv')
    order = orders_df.loc[orders_df['order_id'] == order_id]
    if not order.empty:
        return order.iloc[0]['order_status']
    else:
        return "Order ID not found."

def detect_intent(user_input, context):
    """Detect the intent of the user's input.

        Args:
            user_input (str): The user's input.

        Returns:
            str: The detected intent or an error message.
        """
    prompt = [{"role": "system", "content": "You are a helpful assistant for an e-commerce company named 'BestCompany'. Focus primarily on the user's last messages to determine their request. \
            Identify if the user's message pertains to one of the following services: \
            1. Check Order Status \
            2. Requesting a Human Representative\
            3. Info About Return Policies\
            4. Ending the Conversation\
            5. Other\
            Respond with the corresponding marker:\
            Check Order Status\
            Request Human Representative\
            Info About Return Policies\
            Finished\
            Other."},
            {"role": "user", "content": user_input}]

    # Add the conversation history to the prompt
    for i in range(1, len(context) // 2 + 1):
        user_key = f"user{i}"
        assistant_key = f"assistant{i}"
        if user_key in context:
            prompt.append({"role": "user", "content": context[user_key]})
        if assistant_key in context:
            prompt.append({"role": "assistant", "content": context[assistant_key]})

    # Add the current user input to the prompt
    prompt.append({"role": "user", "content": user_input})

    return api_function(prompt)

def confirm_intent(intent, context):
    """
       Confirm the detected intent (Request Human Representative, Order Status) with the user.

       Args:
           intent (str): The detected intent that needs to be confirmed.
           context (dict): The chat context containing the conversation history.

       Returns:
           str: The response asking the user to confirm the detected intent.
       """
    assistant_key = f"assistant{len(context) // 2 + 1}"
    response = f"I understand that you want help with {intent}. If I'm correct, please type 'yes'. Otherwise, type 'no'."
    context[assistant_key] = response
    info_flags['confirming_intent'] = intent
    return response

def handle_order_status(user_input, context):
    """
        Handle the request to check the status of an order.

        This function processes the user's input to determine if it contains a valid order ID. If the order ID is found,
        it retrieves the order status. If the order ID is not found in the conversation history, it asks the user for
        the order ID.

        Args:
            user_input (str): The input provided by the user.
            context (dict): The chat context containing the conversation history.

        Returns:
            str: The response generated by the chatbot.
        """
    # If waiting for order ID, process the input
    if info_flags.get('waiting_for_order_id', False):
        if re.match(r'^\d{4}[A-Z]$', user_input):
            order_id = re.match(r'^\d{4}[A-Z]$', user_input).group(0)
            order_status = get_order_status(order_id)
            response = f"The status of your order {order_id} is: {order_status}. If you have any other questions, feel free to ask!"
            assistant_key = f"assistant{len(context) // 2 + 1}"
            context[assistant_key] = response
            info_flags['waiting_for_order_id'] = False  # Reset flag
            return response
        else:
            # Reset the flag if the input is not a valid order ID
            info_flags['waiting_for_order_id'] = False
            respond = handle_general_query(context)
            assistant_key = f"assistant{len(context) // 2 + 1}"
            context[assistant_key] = respond
            return respond
    # Check if there's an ID in the conversation history
    for key in reversed(context.keys()):
        if key.startswith("user"):
            msg = context[key]
            if isinstance(msg, str) and re.search(r'.*\b\d{4}[A-Z]\b.*', msg):
                order_id = re.search(r'\b\d{4}[A-Z]\b', msg).group(0)
                order_status = get_order_status(order_id)
                response = f"The status of your order {order_id} is: {order_status}. If you have any other questions, feel free to ask!"
                assistant_key = f"assistant{len(context) // 2 + 1}"
                context[assistant_key] = response
                return response

    # If the order ID is not found, ask the user for the order ID
    response = "To check your order status, I'll need the order ID. It should be *four digits followed by an uppercase letter* (e.g., 0000G)."
    assistant_key = f"assistant{len(context) // 2 + 1}"
    context[assistant_key] = response
    info_flags['waiting_for_order_id'] = True
    return response

def handle_human_representative_request(user_input, context):
    """
       Handle requests for a human representative by collecting necessary user information.

       Args:
           user_input (str): The user's input.
           context (dict): The chat context containing the conversation history.

       Returns:
           str: The response generated by the chatbot.
       """
    # New request - begin with request full name
    if not info_flags.get('waiting_for_name', False) and not info_flags.get('waiting_for_email',False) and not info_flags.get('waiting_for_phone', False):
        info_flags['waiting_for_name'] = True
        response = "To leave a request for a human representative, I'll need three things. First, please enter your full name:"
        assistant_key = f"assistant{len(context) // 2 + 1}"
        context[assistant_key] = response
        return response

    # Collect full name
    if info_flags.get('waiting_for_name', False):
        if user_input.strip():
            info_flags['full_name'] = user_input.strip()
            info_flags['waiting_for_name'] = False
            info_flags['waiting_for_email'] = True
            response = "Great! Now, please enter your email address:"
            assistant_key = f"assistant{len(context) // 2 + 1}"
            context[assistant_key] = response
            return response
        else:
            response = "Full name cannot be empty. Please provide your full name."
            assistant_key = f"assistant{len(context) // 2 + 1}"
            context[assistant_key] = response
            return response

    # Collect email
    if info_flags.get('waiting_for_email', False):
        if re.match(r"[^@]+@[^@]+\.[^@]+", user_input):
            info_flags['email'] = user_input
            info_flags['waiting_for_email'] = False
            info_flags['waiting_for_phone'] = True
            response = "Lastly, please enter your phone number:"
            assistant_key = f"assistant{len(context) // 2 + 1}"
            context[assistant_key] = response
            return response
        else:
            response = "Hmm, that doesn't look like a valid email. Could you please provide a correct email address?"
            assistant_key = f"assistant{len(context) // 2 + 1}"
            context[assistant_key] = response
            return response

    # Collect phone number
    if info_flags.get('waiting_for_phone', False):
        if re.match(r"^\+?\d{10,15}$", user_input):
            info_flags['phone_number'] = user_input
            info_flags['waiting_for_phone'] = False

            contact_info = {
                "full_name": info_flags.get('full_name', ''),
                "email": info_flags.get('email', ''),
                "phone_number": user_input,
                "chat_history": context,
                "timestamp": datetime.datetime.now()
            }

            # Save to CSV
            csv_file = 'contact_info.csv'
            fieldnames = ['full_name', 'email', 'phone_number', 'chat_history', 'timestamp']
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(contact_info)
            response = "Your request to speak with a representative has been forwarded, and someone will get back to you shortly. Is there anything else I can assist you with in the meantime?"
            assistant_key = f"assistant{len(context) // 2 + 1}"
            context[assistant_key] = response
            return response
        else:
            response = "That doesn't seem to be a valid phone number. Please provide your phone number."
            assistant_key = f"assistant{len(context) // 2 + 1}"
            context[assistant_key] = response
            return response
def handle_return_policies_request(user_input, context):
    """
       Handle user requests related to return policies.

       Args:
           user_input (str): The input provided by the user.
           context (dict): The chat context containing the conversation history.

       Returns:
           str: The response generated by the chatbot regarding return policies.
       """
    # Predefined responses for different categories of return policy queries
    response_details = {
        "return policy": "You can return most items within 30 days of purchase for a full refund or exchange. Items must be in their original condition, with all tags and packaging intact. Please bring your receipt or proof of purchase when returning items.",
        "non-returnable items": "Yes, certain items such as clearance merchandise, perishable goods, and personal care items are non-returnable. Please check the product description or ask a store associate for more details.",
        "refund method": "Refunds will be issued to the original form of payment. If you paid by credit card, the refund will be credited to your card. If you paid by cash or check, you will receive a cash refund."
    }

    # Prompt to determine the category of the user's return policy query
    prompt = [{"role": "system", "content": "You are a helpful assistant for an e-commerce company named 'BestCompany'. The user might ask questions about our return policies. Determine which of the following categories the user's message belongs to:\
                \n1. Return Policy: Questions about the general return policy.\
                \n2. Non-Returnable Items: Questions about items that cannot be returned.\
                \n3. Refund Method: Questions about how refunds are processed.\
                \nRespond with one of the following markers based on the user's message:\
                \nReturn Policy\
                \nNon-Returnable Items\
                \nRefund Method.\
                \nPlease choose the best match from these options. Only if none of these apply, respond Other."
               },
              {"role": "user", "content": user_input}]

    # Determine the category of the user's query
    category = api_function(prompt)
    if "Return Policy" in category:
        response = response_details["return policy"]
    elif "Non-Returnable Items" in category :
        response = response_details["non-returnable items"]
    elif "Refund Method" in category:
        response = response_details["refund method"]
    else:
        response = handle_general_query(context)

    assistant_key = f"assistant{len(context) // 2 + 1}"
    context[assistant_key] = response
    return response
def handle_general_query(context):
    """
        Handle general user queries by creating a prompt using the conversation context
        and generating a response using the API.

        Args:
            context (dict): The chat context containing the conversation history.

        Returns:
            str: The response generated by the chatbot.
        """

    # Create the prompt using the conversation context
    prompt = [{"role": "system",
               "content": "You are a helpful chatbot for an e-commerce company named 'BestCompany'. Always be polite and courteous. If you detect that the user is really upset, kindly offer to take their contact information for a later connection with a human representative."}]
    # Add the conversation history to the prompt
    for i in range(1, len(context) // 2 + 1):
        user_key = f"user{i}"
        assistant_key = f"assistant{i}"
        if user_key in context:
            prompt.append({"role": "user", "content": context[user_key]})
        if assistant_key in context:
            prompt.append({"role": "assistant", "content": context[assistant_key]})

    # Generate the response using the API and save it in the context
    print("current prompt:", prompt)
    generated_text = api_function(prompt)
    assistant_key = f"assistant{len(context) // 2 + 1}"
    context[assistant_key] = generated_text
    return generated_text
def handle_customer_query(user_input, context):
    """
        Process the user's input and route to the appropriate handler based on the detected intent.

        Args:
            user_input (str): The input provided by the user.
            context (dict): The chat context containing the conversation history.

        Returns:
            str: The response generated by the chatbot.
        """

    user_key = f"user{len(context) // 2 + 1}"
    context[user_key] = user_input

    # Check if the bot is in the middle of collecting personal information
    if any(info_flags.get(flag, False) for flag in ['waiting_for_name', 'waiting_for_email', 'waiting_for_phone']):
        return handle_human_representative_request(user_input, context)

    # Check if the bot is waiting for an order ID
    if info_flags.get('waiting_for_order_id', False):
        return handle_order_status(user_input, context)

    # Check if the bot is confirming the user's intent for a human representative or order status
    if info_flags.get('confirming_intent', False):
        intent = info_flags.pop('confirming_intent')
        if 'yes' in user_input.strip().lower():
            if intent == "Request Human Representative":
                return handle_human_representative_request(user_input, context)
            elif intent == "Check Order Status":
                return handle_order_status(user_input, context)
        else:
            info_flags.pop('confirming_intent', None)
            return handle_general_query(context)

    # Detect the intent of the user's input
    intent = detect_intent(user_input, context)
    if intent in ["Request Human Representative", "Check Order Status"]:
        return confirm_intent(intent, context)
    elif intent == "Info About Return Policies":
        return handle_return_policies_request(user_input, context)
    elif intent == "Finished":
        response = "It was great talking to you. If you need anything else in the future, don't hesitate to reach out. Have a great day!"
        assistant_key = f"assistant{len(context) // 2 + 1}"
        context[assistant_key] = response
        return response
    else:
        return handle_general_query(context)

@app.route("/")
def home():
    return render_template("frontend.html")
@app.route("/get")
def get_bot_response():
    """
    Handles the GET request for the chatbot response.

    Extracts the user's input message from the request, initializes the conversation context with a welcome message,
    processes the user's input to determine the appropriate response, and returns the chatbot's response.

    Args:
        None

    Returns:
        str: The chatbot's response to the user's input.
    """
    userText = request.args.get('msg')
    response = handle_customer_query(userText, context)
    return response

if __name__ == "__main__":
    # To run the application, please execute this file.
    context = {}
    context["assistant1"] = "Welcome to BestCompany! I'm Anne, your virtual assistant. This is an open-language chat, but I can also handle some requests automatically. Common actions I can assist with include checking order status, providing return policy information, and connecting you with a human representative. How can I help you today?"
    info_flags = {}
    app.run(debug=True)