import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyB5IAY1e0H-lCdM9Nu2zr97zBNxi0UIrak")

def generate_faculty_review(questions, opinions):
    model = genai.GenerativeModel('gemini-pro')

    # Create a template for the AI model to generate the review
    template = """
    Provide a vey breif review for the faculty based on the feedback received from students. 
    The questions along with the corresponding ratings from 1 to 5 are given. 
    Ratinng 1 being very poor and rating 5 being really good.
    Do not use bold letters or make a list. 
    Use plain text within a 200 word limit, just describing the faculty review breifly.
    """

    # Format the template to fit the input format expected by the generative model
    formatted_template = template.strip().replace('\n', ' ')

    # Generate the prompt with questions and opinions
    prompt = formatted_template + "\n".join([f"Question: {question.text} Rating: {opinion.value} " for question, opinion in zip(questions, opinions)])
    print(prompt)
    response = model.generate_content(prompt)

    return response.text
