import os
import base64
import io
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai

class ATSResumeExpert:
    def __init__(self):
        """Initialize the ATSResumeExpert class and configure the Generative AI model."""
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def get_gemini_response(self, input_text, pdf_content, prompt):
        """
        Get the Gemini AI response based on the input text, PDF content, and prompt.

        Args:
            input_text (str): The job description input by the user.
            pdf_content (list): The PDF content converted to image and base64 encoded.
            prompt (str): The prompt to guide the AI response.

        Returns:
            str: The AI-generated response.
        """
        response = self.model.generate_content([input_text, pdf_content[0], prompt])
        return response.text

    def input_pdf_setup(self, uploaded_file):
        """
        Process the uploaded PDF file and convert it to a format suitable for AI input.

        Args:
            uploaded_file (BytesIO): The uploaded PDF file.

        Returns:
            list: The processed PDF content.
        
        Raises:
            FileNotFoundError: If no file is uploaded.
        """
        if uploaded_file is not None:
            # Convert the PDF to image
            images = pdf2image.convert_from_bytes(uploaded_file.read())
            first_page = images[0]

            # Convert to bytes
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
                }
            ]
            return pdf_parts
        else:
            raise FileNotFoundError("No file uploaded")

    def run(self):
        """Run the Streamlit application."""
        st.set_page_config(page_title="ATS Resume Expert")
        st.header("ATS Tracking System")

        input_text = st.text_area("Job Description: ", key="input")
        uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

        if uploaded_file is not None:
            st.write("PDF Uploaded Successfully")

        submit1 = st.button("Tell Me About the Resume")
        submit3 = st.button("Percentage match")

        input_prompt1 = """
        You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
        Please share your professional evaluation on whether the candidate's profile aligns with the role.
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """

        input_prompt3 = """
        You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
        your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
        the job description. First, the output should come as percentage and then keywords missing and last final thoughts.
        """

        if submit1:
            if uploaded_file is not None:
                pdf_content = self.input_pdf_setup(uploaded_file)
                response = self.get_gemini_response(input_text, pdf_content, input_prompt1)
                st.subheader("The Response is")
                st.write(response)
            else:
                st.write("Please upload the resume")

        elif submit3:
            if uploaded_file is not None:
                pdf_content = self.input_pdf_setup(uploaded_file)
                response = self.get_gemini_response(input_text, pdf_content, input_prompt3)
                st.subheader("The Response is")
                st.write(response)
            else:
                st.write("Please upload the resume")


if __name__ == "__main__":
    app = ATSResumeExpert()
    app.run()
