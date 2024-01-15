import os
import sys
from openai import OpenAI

# Ensure the OpenAI API key is set in environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Function to generate security documentation based on user input
def generate_documentation(document_type, user_input):
    try:
        # Construct the prompt for OpenAI based on user input
        prompt = f"Generate a {document_type} document with the following details:\n{user_input}"

        # Generating the document using OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are going to help generate a {document_type} document."},
                {"role": "user", "content": prompt}
            ],
        )
        response_message = response.choices[0].message.content

        # Check if the response is empty
        if not response_message.strip():
            print("Received an empty response from OpenAI. Please try again.")
            return None

        return response_message.strip()
    except Exception as e:
        print(f"Error generating documentation: {e}")
        return None

# Function to save the generated documentation as a Markdown or text file
def save_documentation(document, document_type, format_option):
    try:
        if format_option == "markdown":
            # Add Markdown formatting
            formatted_document = f"## {document_type}\n\n{document}"
        else:
            formatted_document = document
        
        save_option = input("Do you want to save the documentation? (yes/no): ").strip().lower()
        if save_option == "yes":
            file_extension = ".md" if format_option == "markdown" else ".txt"
            file_name = f"{document_type.replace(' ', '_').lower()}_documentation{file_extension}"
            with open(file_name, "w") as file:
                file.write(formatted_document)
            print(f"Documentation saved as {file_name}")
        else:
            print("Documentation not saved.")
    except Exception as e:
        print(f"Error saving documentation: {e}")

def main():
    print("Welcome to the Documentation Generator!")
    
    while True:
        # Prompt the user for the type of securty document they want to generate
        document_type = input("Enter the type of document (e.g., Security Policy, Incident Response Plan): ")

        # Prompt the user for specific details or requirements
        user_input = input("Enter the specific details or requirements for the document: ")

        # Prompt the user for the desired format (Markdown or plain text)
        format_option = input("Select the format for the document (markdown/text): ").strip().lower()

        # Generate the documentation based on user input
        generated_document = generate_documentation(document_type, user_input)

        if generated_document:
            print("\nGenerated Documentation:")
            print(generated_document)

            # Save the documentation based on user's preference
            save_documentation(generated_document, document_type, format_option)

        # Ask if the user wants to generate another document
        another_document_option = input("Do you want to generate another document? (yes/no): ").strip().lower()
        if another_document_option != "yes":
            break

if __name__ == "__main__":
    main()
