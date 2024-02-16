from flask import Flask, request, render_template_string, redirect, url_for
import requests
import datetime
import os

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


app = Flask(__name__)

# Updated form template with Tailwind CSS
FORM_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Odoo Backup</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
        <h2 class="mb-4 text-xl font-bold text-gray-900">Odoo Backup Form</h2>
        <form method="post" class="space-y-4">
            <div>
                <label for="dbname" class="block text-sm font-medium text-gray-700">Database Name:</label>
                <input type="text" id="dbname" name="dbname" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            <div>
                <label for="password" class="block text-sm font-medium text-gray-700">Admin Password:</label>
                <input type="password" id="password" name="password" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            <input type="submit" value="Backup" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def backup_form():
    if request.method == 'POST':
        # Extract form data
        dbname = request.form['dbname']
        password = request.form['password']
        
        # Perform backup
        BACK_DIR = os.path.dirname(os.path.abspath(__file__))
        #Change ip/localhost here
        URL = 'https://localhost:8069/web/database/backup'
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_filename = f"{date}_{dbname}.zip"
        data = {
            'master_pwd': password,
            'name': dbname,
            'backup_format': 'zip'
        }
        
        response = requests.post(URL, data=data, verify=False)

        
        if response.ok:
            with open(os.path.join(BACK_DIR, backup_filename), 'wb') as f:
                f.write(response.content)
            return f'<div>Backup created successfully: {backup_filename}</div>'
        else:
            return f'<div>Failed to create backup, HTTP Status Code: {response.status_code}</div>'
        
    return render_template_string(FORM_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
