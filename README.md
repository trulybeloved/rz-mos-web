# Re:ZERO MoS Web

A beautified and searchable version of the [WCT](https://witchculttranslation.com) Manual of Style for translations of the free unlicensed [japanese webnovel](https://ncode.syosetu.com/n2267be) "Re:ZERO - Starting Life in Another World from Zero".

Data Sources and Updates by @kroatoanjp

## Hosted Build

https://rzmosweb.pages.dev

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

# Python MoS Parser

## To obtain the `credentials.json` file required for using the Google Drive API, follow these steps:

---

### Step 1: Enable Google Drive API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Log in with your Google account.
3. Create a new project or select an existing one:
   - Click the project dropdown at the top and select **New Project**.
   - Name your project and click **Create**.

---

### Step 2: Enable the Drive API

1. In the Cloud Console, navigate to **APIs & Services** > **Library**.
2. Search for "Google Drive API" and click on it.
3. Click the **Enable** button.

---

### Step 3: Create OAuth 2.0 Credentials

1. Navigate to **APIs & Services** > **Credentials** in the Cloud Console.
2. Click on **Create Credentials** and select **OAuth client ID**.
   - If prompted to configure the OAuth consent screen, follow the instructions:
     - Choose **External** as the user type.
     - Fill in the required fields (app name, support email, etc.) and save.
3. Choose **Desktop app** as the application type.
4. Click **Create** and then **Download JSON**. Save this file as `credentials.json`.

---

### Step 4: Place the `credentials.json` File

1. Save the `credentials.json` file in a directory accessible to your Python script.
2. Use the full path to the file when calling the `download_google_docx` function.

---

### Step 5: Authenticate Locally

The first time you run the script:

1. You’ll be prompted to visit a URL and grant your app access to your Google Drive.
2. The library will save a token (e.g., `token.json`) for future use, so you don’t need to log in every time.

---

### Notes

- Make sure the Google account you use has access to the file you want to download.
- The credentials are sensitive—do not share the `credentials.json` file publicly.
- For more details, see Google's [Python Quickstart Guide](https://developers.google.com/drive/api/quickstart/python).


# Service Account Setup Guide

## What is a Service Account?
A service account is a special Google account that belongs to your application (not a user). It allows automated access without requiring periodic OAuth login.

## Setup Steps

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one

### 2. Enable Required APIs
Enable these APIs in your project:
- Google Drive API
- Google Docs API
- Google Sheets API
- Google Slides API

You can enable them here: https://console.cloud.google.com/apis/library

### 3. Create a Service Account
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "Create Service Account"
3. Enter a name (e.g., "my-app-service-account")
4. Click "Create and Continue"
5. Skip the optional "Grant access" step (click "Continue")
6. Skip the optional "Grant users access" step (click "Done")

### 4. Create and Download the Service Account Key
1. Click on the service account you just created
2. Go to the "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" format
5. Click "Create"
6. The JSON key file will download automatically - **KEEP THIS FILE SECURE!**
7. Rename it to something like `service-account-key.json`

### 5. Share Files with the Service Account

**IMPORTANT:** Your service account needs permission to access files!

The service account has an email address like:
`my-app-service-account@my-project-123456.iam.gserviceaccount.com`

To give it access to files:

#### Option A: Share Individual Files
1. Open the Google Doc/Sheet/Slide you want to access
2. Click "Share"
3. Enter the service account email
4. Give it "Viewer" or "Editor" permission
5. Click "Send"

#### Option B: Use a Shared Folder
1. Create a Google Drive folder
2. Share the folder with the service account email
3. Place all files you want to access in this folder

#### Option C: Domain-Wide Delegation (G Workspace Only)
If you have a Google Workspace account, you can enable domain-wide delegation:
1. Go to service account details
2. Check "Enable Google Workspace Domain-wide Delegation"
3. Follow G Workspace admin setup to authorize scopes

## Security Best Practices

1. **Never commit the service account key to version control!**
   Add to `.gitignore`:
   ```
   service-account-key.json
   *.json
   ```

2. **Store the key securely:**
   - Use environment variables
   - Use secret management services (AWS Secrets Manager, Google Secret Manager, etc.)
   - Set restrictive file permissions: `chmod 600 service-account-key.json`

3. **Limit service account permissions:**
   - Only enable APIs you need
   - Use read-only scopes when possible
   - Regularly audit access

## Usage Example

```python
from google_workspace_service_account import get_file_as_json

# The file must be shared with your service account email!
doc_json = get_file_as_json(
    shared_link="https://docs.google.com/document/d/YOUR_FILE_ID/edit",
    service_account_file="service-account-key.json",
    output_file="output.json"
)
```

## Troubleshooting

### Error: "The caller does not have permission"
- Make sure you shared the file with the service account email
- Check that you enabled the required APIs

### Error: "Request had insufficient authentication scopes"
- Verify all required APIs are enabled in Google Cloud Console

### Error: "File not found"
- The file must be shared with the service account
- Check the file ID is correct

## Environment Variable Method (More Secure)

Instead of passing the file path directly, you can use environment variables:

```python
import os
from google.oauth2 import service_account

# Set environment variable with the path
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

creds = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=SCOPES
)
```

## Comparison: OAuth vs Service Account

| Feature | OAuth (User Account) | Service Account |
|---------|---------------------|-----------------|
| User interaction | Required periodically | None |
| Best for | Personal use, user-specific data | Automation, server apps |
| File access | User's files automatically | Must be explicitly shared |
| Setup complexity | Moderate | Higher initial setup |
| Security | User controls access | Key file must be secured |