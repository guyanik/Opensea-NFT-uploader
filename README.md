## Requirements

- `pip install -r requirements.txt`
- Make sure you have chrome driver installed.
- Create `.env` from `.example.env` with required keys.

### Understanding the .env

- EXTENSION_PATH: In our program, we're running a selenium based browser (chrome driver here) and usually in automated environment we don't have access to extensions, so get the access.
   - Navigate to chrome://extensions/
Click ‘Pack extension’ and enter the local path to the Metamask extension. This will generate a .crx file. Also, make a note of Extension ID.
   - Now the path to this '.crx' file is the value of this field.
- RECOVERY_CODE: Recovery code of your wallet cause we need to login into your metamask.
- PASSWORD: Metamask's password.
- CHROME_DRIVER_PATH: To run chromium, you need to download the chrome driver and it's path will be the value. (https://chromedriver.chromium.org/downloads)
