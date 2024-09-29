# The Community OutReach Network

The Community OutReach Network is a web application designed to empower volunteers and community members to report and manage local issues using a user-friendly map interface and Google Places API for location identification.

Bred from the challenges of ShellHacks '24.

[Live Demo](https://communityoutreachnet.work/)

## Features

- User Authentication via Auth0
- Report issues with location autocomplete and optional attachments
- Manage reported issues
- Display issues on a map with Google Maps API
- Material Design Dark Theme for a sleek appearance
- View resolved issues under user profiles

## Technologies Used

- **Backend:** Flask, Google Firebase Firestore
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Authentication:** Auth0
- **APIs:** Google Maps JavaScript API, Google Places API

## Prerequisites

- Python 3.7 or higher
- Flask
- Firebase Account
- Auth0 Account
- Google Cloud Platform Account

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/chillwave/CORN.git
    cd CORN
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up Google Cloud APIs:**

    - Enable **Google Maps JavaScript API** and **Google Places API** in your Google Cloud Console.

5. **Set up Firebase:**

    - Create a Firebase project and Firestore database.
    - Download the service account key JSON file and save it as `firebase-key.json` in the root of your project.

6. **Set up Auth0:**

    - Create an Auth0 application.
    - Configure Allowed Callback URLs and Allowed Logout URLs.

7. **Set up environment variables:**

    Create a `.env` file in the root of your project and add the following:

    ```env
    DATABASE_URL=sqlite:///community.db
    GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
    AUTH0_CLIENT_ID=your_auth0_client_id_here
    AUTH0_CLIENT_SECRET=your_auth0_client_secret_here
    AUTH0_DOMAIN=your_auth0_domain_here
    ```

8. **Run the Flask application:**

    ```bash
    python app.py
    ```

9. **Access the application:**

    Open your browser and navigate to `http://localhost:5000`.

## Directory Structure

```
CORN/
├── app.py
├── config.py
├── models.py
├── routes.py
├── schemas.py
├── firebase_config.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   └── uploads/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── report_issue.html
│   ├── manage_issues.html
│   └── profile.html
├── .env
├── requirements.txt
└── README.md
```

## Usage

### Reporting an Issue

1. **Log in:**
    - Use the "Login" link in the navigation bar to authenticate via Auth0.

2. **Report an Issue:**
    - Navigate to the "Report Issue" page.
    - Fill in the description, place (with autocomplete), and optionally attach a file.
    - Submit the form to report the issue.

### Managing Issues

1. **Manage Issues:**
    - Navigate to the "Manage Issues" page.
    - View the list of reported issues.
    - Click "Resolve Issue" to mark an issue as resolved.

2. **View Resolved Issues:**
    - Navigate to your profile page to view resolved issues.

## Contribution

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

## To-Do

- Timestamp case entries
- case number assignment
- Add an about page
- Add search bar functionality
- Center map based on client geolocation
- Client-to-volunteer chat platform
- Re-enable CDN caching (CF ZeroTrust)