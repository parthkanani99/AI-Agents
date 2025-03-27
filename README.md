


# 📧 Gmail Agent with LangChain + Streamlit

This project lets you generate and send professional emails (with inline AI-generated images and signature) using **OpenAI** and **Gmail API** through a simple **Streamlit interface**.

## 🌟 Features

- 🔥 Uses OpenAI to generate email body & subject
- 🎨 Adds auto-generated image from your prompt
- 📬 Sends emails through Gmail API with inline image
- 🖋️ Adds signature automatically

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gmail-agent.git
cd gmail-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Add your **OpenAI API key** to `.env`:

```env
OPENAI_API_KEY=your-openai-api-key
```

---

## 🔐 Google API Setup

### Step 1: Create `credentials.json`

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Credentials**.
4. Click **+ Create Credentials** > **OAuth client ID**.
5. Choose **Desktop App** as application type.
6. Download the OAuth 2.0 credentials — this is your `credentials.json`.

   Example structure:
   ```json
   {
     "installed": {
       "client_id": "YOUR_CLIENT_ID",
       "project_id": "YOUR_PROJECT_ID",
       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
       "token_uri": "https://oauth2.googleapis.com/token",
       "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
       "client_secret": "YOUR_CLIENT_SECRET",
       "redirect_uris": ["http://localhost"]
     }
   }
   ```

7. Save this file as `credentials.json` in the root directory of the project.

---

### Step 2: Generate `token.json`

Once you have the `credentials.json` file in place, the app will automatically prompt you to authenticate with your Google account the first time you run it.

After successful authentication, a `token.json` file will be created automatically to store your access and refresh tokens for the Gmail API.

> `token.json` should **not** be committed to Git.

---

## 🧪 Running the App

```bash
streamlit run new.py
```

- Enter your email idea
- Click **"✨ Generate Email + Image"**
- Provide recipient addresses
- Click **"📤 Send Email"**

---

## 📂 File Structure

```bash
gmail-agent/
│
├── new.py                # Main Streamlit app
├── .env                  # Your OpenAI API key (not committed)
├── .env.example          # Example template for others
├── credentials.json      # Google OAuth client secrets (not committed)
├── token.json            # Created after first login (not committed)
├── requirements.txt      # All dependencies
├── README.md             # You're reading it!
└── .gitignore            # Excludes secrets and Python junk
```

---

## ⚠️ Security Notes

- Never commit your `.env`, `credentials.json`, or `token.json`.
- `.gitignore` is configured to keep your secrets safe.

---

