# UnityLink: AI-Driven Community Resource Orchestrator

**UnityLink** is a smart, hyper-local community assistance platform designed to bridge the gap between people in need (**Users**) and local service providers (**Volunteers**). Developed for the **AMD Slingshot Regional Ideathon**, it transforms scattered community data into an actionable real-time matching network.

---

## 🚀 The Problem
Local NGOs and community groups often struggle with scattered information. Valuable data about local needs is often lost in paper surveys or fragmented digital sheets, making it difficult to connect help where it is needed most.

## 💡 The Solution
UnityLink provides a centralized, automated system that:
1.  **Aggregates Data:** Collects real-time needs and offers via a streamlined web interface.
2.  **Handles Integrity:** Features an 'Upsert' mechanism to prevent duplicate entries based on unique contact numbers.
3.  **Smart Matching:** Uses a proximity-based algorithm to match users and volunteers within the same or neighboring Pincodes.

---

## 🛠️ Tech Stack
- **Backend:** Python (Flask)
- **Database:** Google Sheets (via GSpread API)
- **Frontend:** HTML5, CSS3, JavaScript (Asynchronous Fetch API)
- **Infrastructure:** Google Cloud Platform (Service Accounts)

---

## ⚙️ Key Features
- **Pincode Proximity Logic:** Automatically ranks matches by geographical closeness (Nearest First).
- **Duplicate Prevention:** Uses contact numbers as unique identifiers to maintain a clean database.
- **Real-time Synchronization:** Direct integration with Google Sheets for live administrative monitoring.
- **Asynchronous UI:** Data is submitted and results are fetched without page refreshes for a seamless UX.

---

## 📁 Project Structure
```text
unitylink/
├── app.py              # Flask server & Matching logic
├── credentials.json    # Google Cloud Service Account keys (Keep Private!)
├── static/
│   ├── home.css        # Styles for the landing page
│   ├── user.css        # Styles for the User portal
│   └── volunteer.css   # Styles for the Volunteer portal
├── templates/
│   ├── home.html       # Landing page
│   ├── user.html       # User registration & search
│   └── volunteer.html  # Volunteer registration & search
└── .gitignore          # Prevents credentials.json from being pushed to GitHub
