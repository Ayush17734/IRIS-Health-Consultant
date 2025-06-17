# -*- coding: utf-8 -*-
# health/iris_core.py

import google.generativeai as genai
from decouple import config

genai.configure(api_key=config("GEMINI_API_KEY"))

def iris_health_consultant(user_query, user_name="there", conversation_context=""):
    try:
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

        prompt = f"""
        You are IRIS, a warm and empathetic virtual health assistant. 🩵
        Respond with kindness, offer support, and include helpful emojis when relevant.
        Address the user by name: {user_name}.

        Conversation so far:
        {conversation_context}

        Now the user says: "{user_query}"
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"IRIS: Oops! Something went wrong. ({str(e)})"

