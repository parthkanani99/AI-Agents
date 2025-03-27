from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit
from langchain_community.tools.gmail.utils import get_gmail_credentials
import streamlit as st
import os
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from PIL import Image
import requests
from io import BytesIO
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from googleapiclient.discovery import build

# Step 1: Configure Streamlit App
st.title("📧 Gmail Agent with Langchain + Inline Image")
st.write("Describe your email and get a generated email with an inline image and signature sent via Gmail!")

# Step 2: Set OpenAI API Key
os.environ['OPENAI_API_KEY'] = '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'

# Step 3: Gmail Credentials
credentials_path = r"C:\\Users\\parth\\OneDrive\\Documents\\Gmail Agent\\.venv\\Gmail Agent\\credentials.json"

try:
    # Get Gmail Credentials
    credentials = get_gmail_credentials(client_secrets_file=credentials_path)
    toolkit = GmailToolkit(credentials=credentials)
    tools = toolkit.get_tools()

    # OpenAI LLM
    llm = OpenAI(temperature=0)

    # Step 4: User Input
    user_input = st.text_area("💬 What is your email about?", key="email_content")
    email_output = ""

    # Step 5: Generate Email & Image
    if st.button("✨ Generate Email + Image"):
        try:
            # Prompt for email body (signature added manually)
            email_prompt_template = PromptTemplate.from_template(
                "Generate a professional email template based on this idea:\n\n"
                "{idea}\n\n"
                "Include a subject line, greeting, and body."
            )
            formatted_prompt = email_prompt_template.format(idea=user_input)

            # Get response from LLM and manually append signature
            email_output_raw = llm.invoke(formatted_prompt)
            email_output = f"{email_output_raw.strip()}\n\nBest regards,\nParth Kanani"

            # Display generated email
            st.subheader("📨 Generated Email")
            st.write(email_output)

            # Generate Image
            image_prompt = f"An illustration representing: {user_input}"
            image_url = f"https://image.pollinations.ai/prompt/{image_prompt.replace(' ', '%20')}"
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            image_path = "generated_image.png"
            image.save(image_path)

            st.subheader("🖼️ Generated Image")
            st.image(image, caption="Visual Representation")

            # Store in session for email sending
            st.session_state["email_output"] = email_output
            st.session_state["image_path"] = image_path
            st.session_state["user_input"] = user_input

        except Exception as e:
            st.error(f"Error generating content: {e}")

    # Step 6: Send Email with Inline Image
    if "email_output" in st.session_state:
        recipients = st.text_input("📬 Enter recipient email addresses (comma-separated):")
        if st.button("📤 Send Email"):
            try:
                # Extract subject and body
                lines = st.session_state["email_output"].split("\n")
                subject_line = next((line for line in lines if "Subject:" in line), "")
                subject = subject_line.replace("Subject:", "").strip() or "No Subject"
                body_text = "\n".join([line for line in lines if "Subject:" not in line and line.strip() != ""])

                # Build HTML body with embedded image
                html_body = f"""
                <html>
                    <body>
                        <p>{body_text.replace('\n', '<br>')}</p>
                        <img src="cid:image1"><br>
                    </body>
                </html>
                """

                # Format recipient list
                recipient_list = [email.strip() for email in recipients.split(",") if email.strip()]

                # Create MIME message
                message = MIMEMultipart("related")
                message["Subject"] = subject
                message["To"] = ", ".join(recipient_list)
                message.attach(MIMEText(html_body, "html"))

                # Embed image if exists
                if "image_path" in st.session_state:
                    with open(st.session_state["image_path"], "rb") as img_file:
                        img = MIMEImage(img_file.read())
                        img.add_header("Content-ID", "<image1>")
                        img.add_header("Content-Disposition", "inline", filename="image.png")
                        message.attach(img)

                # Encode and send via Gmail API
                raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
                service = build("gmail", "v1", credentials=credentials)
                service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

                st.success("✅ Email sent with inline image and signature!")

            except Exception as e:
                st.error(f"Error sending email: {e}")

except Exception as e:
    st.error(f"An error occurred: {e}")
