# ATS Resume Expert

This project uses Google Gemini AI to evaluate resumes against job descriptions. The application is built with Streamlit and leverages PDF processing and generative AI for content evaluation.

## Features

- Upload a PDF resume and input a job description.
- Get a professional evaluation of the resume based on the job description.
- Calculate the percentage match between the resume and job description, highlighting missing keywords.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sairam-penjarla/Google-gemini-Resume-ATS-system.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Google-gemini-Resume-ATS-system
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables. Create a `.env` file in the root directory and add your Google API key:

    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    ```

## Usage

Run the Streamlit application:

```bash
streamlit run main.py
