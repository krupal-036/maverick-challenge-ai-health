# **AI for Inclusive Healthcare Access**

[![Status](https://img.shields.io/badge/Status-Live-brightgreen)](https://maverick-challenge-ai-health.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django)](https://www.djangoproject.com/)

**Live Application URL: [https://maverick-challenge-ai-health.onrender.com](https://maverick-challenge-ai-health.onrender.com)**

This project is a submission for the **Maverick Effect AI Challenge**, addressing the problem statement: **"AI for Inclusive Healthcare Access"**.

It is a fully functional web-based telemonitoring system designed to assist communities in remote areas. The platform leverages AI to provide instant access to healthcare information and teleconsultations, helping to reduce disparities in healthcare services and empower users to take control of their health.

## **Vision & Purpose**

The core mission of this project is to bridge the healthcare gap for remote and underserved communities. By providing an intelligent, accessible first point of contact, we aim to:
*   **Democratize Health Information:** Offer AI-driven insights that are easy to understand.
*   **Facilitate Professional Care:** Seamlessly connect patients with approved medical professionals.
*   **Reduce Barriers to Access:** Operate on a modern, low-overhead architecture that is both scalable and cost-effective.

## **Key Features**

*   **🤖 AI-Powered Symptom Checker**: Patients describe symptoms in natural language and receive a potential diagnosis and recommendations from the **Google Gemini API**.
*   **🧑‍⚕️ Multi-Role System**: Three distinct user roles (Patient, Doctor, Admin) with unique dashboards, permissions, and responsibilities.
*   **🩺 End-to-End Teleconsultation Workflow**: A complete system for patients to request consultations and for doctors to review and manage these requests.
*   **⚡ Headless Architecture**: All application data is managed through the **Notion API**, demonstrating a modern, serverless-style web architecture without a traditional SQL database.
*   **🛡️ Admin Governance**: A comprehensive admin dashboard to approve new doctor registrations and manage all user data, ensuring quality control.
*   **⚙️ Robust & Secure**: Implements Django's built-in security features, environment variable management for secrets, and is configured for production deployment.
*   **🔄 Dynamic API Key Rotation**: Automatically rotates Gemini API keys to handle rate limits and ensure high availability of the AI service.

## **Project Structure**

The project is organized with a clean, scalable structure to promote maintainability and separation of concerns.

```
maverick-challenge-ai-health/
├── .gitignore              # Specifies files to be ignored by Git
├── README.md               # This documentation file
├── .env                    # Environment variables File
├── .env(Example)           # Environment variables File(Example)
├── build.sh                # Automated build script for Render deployment
├── manage.py               # Django's command-line utility
├── doctors.csv             # Notion Database file
├── consultations.csv       # Notion Database file
├── mainadmin.csv           # Notion Database file
├── patients.csv            # Notion Database file
├── render.yaml             # Infrastructure as Code for Render deployment
├── requirements.txt        # List of Python dependencies
│
└── aihealth/               # The core Django application
    ├── settings.py         # Main project settings (configured for production)
    ├── urls.py             # Root URL configuration
    │
    ├── gemini/             # Handles all Gemini AI chatbot logic
    │   ├── api_key_rotator.py
    │   └── gemini_chatbot.py
    │
    ├── notion/             # Encapsulates all Notion API interactions (CRUD services)
    │   ├── admin_service.py
    │   ├── base_service.py
    │   ├── consultation_service.py
    │   ├── doctor_service.py
    │   └── patient_service.py
    │
    ├── static/             # Contains all static assets (CSS, JS)
    │   ├── css/style.css
    │   └── js/script.js
    │
    ├── templates/          # Contains all HTML templates for the UI
    │   ├── admin_dashboard.html
    │   ├── base.html
    │   ├── doctor_dashboard.html
    │   ├── login.html 
    │   ├── patient_dashboard.html
    │   ├── registration.html
    │   ├── registration_doctor.html    
    │   └── registration_patient.html
    │
    └── views/              # Contains the application logic for each page
        ├── admin_views.py
        ├── auth_views.py
        ├── doctor_views.py
        └── patient_views.py
```

---

## **Local Development Setup**

Follow these steps to run a local instance of the project for development or testing.

### **1. Prerequisites**
*   Python 3.10+
*   Git
*   A Notion account
*   A Google account for Gemini API keys

### **2. Clone & Install Dependencies**
```bash
# Clone the repository
git clone https://github.com/krupal-036/maverick-challenge-ai-health.git
cd maverick-challenge-ai-health

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install all required packages
pip install -r requirements.txt
```

### **3. Configure Notion**
1.  **Create an Integration**: Go to [notion.so/my-integrations](https://www.notion.so/my-integrations) to create a new integration. Grant it **Read, Update, and Insert** content capabilities. Copy the secret token to get your `NOTION_API_KEY`.
2.  **Create Databases via CSV**: In your Notion workspace, use the **`Import`** feature to import the provided CSV files (`patients.csv`, `doctors.csv`, etc.). This will create the required databases with sample data.
3.  **Correct Property Types**: **This is a crucial step.** After importing, go into each new database and manually set the correct property type (`Email`, `Select`, `Date`, `Checkbox`) for each column as needed. The application will fail if the types are incorrect.
4.  **Connect Integration**: For each of the four databases, click the `...` menu, select **`+ Add connections`**, and add your new integration.
5.  **Get Database IDs**: Open each database as a full page and copy its unique 32-character ID from the URL.

### **4. Configure Environment File**
Create a file named `.env` in the project root and populate it with your keys and IDs.

```
# .env - Local Development Configuration

SECRET_KEY='generate-a-random-key-for-local-use'
DEBUG=True

NOTION_API_KEY='secret_YOUR_NOTION_KEY'
NOTION_MAINADMIN_DB_ID='your-mainadmin-database-id'
NOTION_DOCTOR_DB_ID='your-doctor-database-id'
NOTION_PATIENT_DB_ID='your-patient-database-id'
NOTION_CONSULTATION_DB_ID='your-consultation-database-id'

GEMINI_API_KEYS='YOUR_GEMINI_KEY_1,YOUR_GEMINI_KEY_2'
```

### **5. Create Your Admin User**
To log in as an administrator, you must create a user manually in your `mainadmin` Notion database.
1.  **Generate a Hashed Password**: Create and run a temporary Python script (`hash_password.py`) to generate a secure `bcrypt` hash for your password.
    ```python
    import bcrypt
    password = b"MyAdminPassword123!"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    print(hashed.decode('utf-8'))
    ```
2.  **Add a New Row** in your `mainadmin` Notion database with your details and paste the generated hash into the `password_hash` column.

### **6. Run the Application**
```bash
# Run migrations for Django's session framework and other built-in apps
python manage.py migrate

# Start the development server
python manage.py runserver

# Open your browser to http://127.0.0.1:8000/
```

---

## **Live Demo Walkthrough**

To experience the full workflow of the application, follow these steps:

1.  **Register as a Patient**: Create a new patient account.
2.  **Use the AI Symptom Checker**: On the patient dashboard, enter symptoms like "I have a sore throat and a slight fever" and click "Get Analysis".
3.  **Register as a Doctor**: Log out, then register a new doctor account. Note that you cannot log in yet.
4.  **Log in as Admin**: Use your admin credentials to log in.
5.  **Approve the Doctor**: On the admin dashboard, find the newly registered doctor in the "Approve New Doctors" panel and click "Approve".
6.  **Log in as the Doctor**: Log out of the admin account and log in with the doctor account you just approved. The dashboard will be empty.
7.  **Request a Consultation**: Log out and log back in as the patient. Now, select the newly approved doctor from the dropdown and send a consultation request.
8.  **Accept the Consultation**: Log back in as the doctor. You will now see the pending request. Click "Accept".
9.  **View Final Status**: Log back in as the patient. In your "My Consultation History," you will see the request's status is now "Accepted".

---
## **Deployment on Render**

This project is configured for a seamless "Infrastructure as Code" deployment on Render using the `render.yaml` and `build.sh` files.

1.  **Push to GitHub**: Commit all project files to a new GitHub repository.
2.  **Connect to Render**:
    *   Log in to the [Render Dashboard](https://dashboard.render.com/).
    *   Click **New +** and select **Blueprint Instance**.
    *   Connect the GitHub repository you just created. Render will automatically detect and parse your `render.yaml` file.
3.  **Add Secrets**: Before finalizing, create a new **Environment Group** to store your secrets. Add all the key-value pairs from your local `.env` file here. Render will inject them securely during the build. **Do not commit your `.env` file.**
4.  **Deploy**: Click **"Create New Blueprint Instance"**. Render will automatically run the `build.sh` script to set up your application and then use the `startCommand` to launch it.

Any future `git push` to your main branch will trigger a new automatic deployment.
