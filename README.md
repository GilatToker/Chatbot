## 07.2024

# Conversational Agent for E-commerce

## Project Overview
his repository contains the files and documentation for the development of a conversational agent (chatbot) aimed at handling customer support queries for an e-commerce platform. The main goal of this project is to create a chatbot using a Large Language Model (LLM) that can manage multi-turn conversations effectively and provide accurate responses regarding order status, return policies, and general customer inquiries. 

## Project Goals and Functionalities
The goal of this project is to develop a chatbot capable of handling customer inquiries in real-time, providing meaningful responses regarding:
- Order Status: Retrieve and communicate the status of a customer’s order.
- Return Policies: Provide specific details about return policies, including conditions for refunds and non-returnable items.
- Requesting a Human Representative: When needed, assist users in connecting with a human representative for more personalized help.

### Additional Functionalities
To enhance the user experience, we implemented a few additional features such as:

- Suggesting a human representative when detecting customer dissatisfaction.
- Retrieving previous details, such as order IDs, from chat history to streamline conversation flow.
- Asking for confirmation before requesting personal information.

## Method
The chatbot utilizes the GPT-4o language model, known for its speed and cost-effectiveness. The system integrates predefined responses for frequently asked questions related to order status, returns, and human representative requests.

To provide a user-friendly interaction, we employed Flask, a lightweight web application framework, to enable a web-based interface for the chatbot.

## Evaluation Methodology
The chatbot's performance was evaluated using a manually created dataset that includes dialogue samples covering all of the required functionalities. Each response from the chatbot was evaluated based on:
- Accuracy: Whether the response met user expectations.
- Relevance: How well the response matched the user's query.
- User Satisfaction: The overall likelihood of the user being satisfied with the response.

## Below is a preview of the chatbot interface.
<table>
  <tr>
    <td>
      <img src="Screenshot.png" width="550"/>
    </td>
  </tr>
</table> 

#### For a more in-depth understanding of the methodology, approach, and evaluation, please refer to the complete report provided in Final report.pdf.
