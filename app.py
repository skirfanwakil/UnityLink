import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- SMART GOOGLE SHEETS SETUP (Vercel + Local) ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Vercel par hum 'GOOGLE_CREDENTIALS' naam ka variable use karenge
creds_raw = os.environ.get('GOOGLE_CREDENTIALS')

try:
    if creds_raw:
        # Agar Vercel environment mein credentials mil gayi
        creds_info = json.loads(creds_raw)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    else:
        # Local system ke liye credentials.json file
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    
    client = gspread.authorize(creds)
    SHEET_ID = "11k63x80AQ9mkUjpyHe1QXqum4mreNGOfWwCA7gjysao"
    sheet = client.open_by_key(SHEET_ID).sheet1
except Exception as e:
    print(f"Database Connection Error: {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user')
def user_page():
    return render_template('user.html')

@app.route('/volunteer')
def volunteer_page():
    return render_template('volunteer.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        
        # --- 🧹 DATA CLEANING LAYER ---
        # 1. Names aur HelpType ko Title Case mein convert karna (e.g., 'food' -> 'Food')
        user_name = str(data.get('name')).strip().title()
        user_help = str(data.get('helpType')).strip().title()
        
        # 2. Contact number se spaces hatana aur string mein rakhna
        user_contact = str(data.get('contact')).replace(" ", "").strip()
        
        # 3. Pincode ko clean karke integer mein badalna
        user_pin_raw = str(data.get('pincode')).strip()
        user_pin = int(user_pin_raw) if user_pin_raw.isdigit() else 0
        
        user_role = data.get('role')

        # --- STEP 1: SMART DUPLICATE CHECK ---
        all_records = sheet.get_all_records()
        already_exists = False
        
        for record in all_records:
            # Clean database values while checking for better accuracy
            db_contact = str(record.get('Contact')).replace(" ", "").strip()
            db_role = str(record.get('Role')).strip()
            
            if db_contact == user_contact and db_role == user_role:
                already_exists = True
                break

        if not already_exists:
            # Clean row insert ho rahi hai
            new_row = [user_name, user_help, user_contact, user_pin, user_role]
            sheet.append_row(new_row)
            status_msg = "success"
        else:
            status_msg = "already_existed"
        
        # --- STEP 2: MATCHING LOGIC ---
        all_records = sheet.get_all_records()
        matches = []
        opposite_role = "Volunteer" if user_role == "User" else "User"
        
        for record in all_records:
            # Cleaning the DB values during comparison too
            db_role = str(record.get('Role')).strip()
            db_help = str(record.get('HelpType')).strip().title()

            if db_role == opposite_role and db_help == user_help:
                try:
                    db_pin_val = str(record.get('PinCode', 0)).strip()
                    db_pin = int(db_pin_val) if db_pin_val.isdigit() else 0
                    
                    distance = abs(user_pin - db_pin)
                    record['distance'] = distance
                    matches.append(record)
                except:
                    continue
        
        # Sorting matches by nearest distance
        matches = sorted(matches, key=lambda x: x.get('distance', 9999))
        
        return jsonify({
            "status": "success", 
            "message": status_msg, 
            "matches": matches
        })

    except Exception as e:
        print(f"Cleaning/Submission Error: {e}")
        return jsonify({"status": "error", "message": str(e)})

# Vercel needs this to handle serverless execution
if __name__ == '__main__':
    app.run(debug=True)
