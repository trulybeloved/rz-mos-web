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
