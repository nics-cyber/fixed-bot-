To run the Discord bot, follow these steps:

---

### **Step 1: Install Python**
Ensure you have Python installed on your system. You can check by running:
```bash
python3 --version
```
If Python is not installed, download and install it from [python.org](https://www.python.org/).

---

### **Step 2: Install Required Dependencies**
The bot requires the `discord.py` library and `tmate` for SSH sessions. Install them using the following commands:

1. Install `discord.py`:
   ```bash
   pip install discord.py
   ```

2. Install `tmate`:
   - On Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install tmate
     ```
   - On other systems, refer to the [tmate installation guide](https://tmate.io/).

---

### **Step 3: Set Up the Bot**
1. **Create a Discord Bot**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a new application and add a bot to it.
   - Copy the bot token (this is your `TOKEN` in the code).

2. **Update the Configuration**:
   - Replace `YOUR_DISCORD_BOT_TOKEN` in the code with your actual bot token.
   - Update `ALLOWED_CHANNEL_IDS` and `ALLOWED_ROLE_IDS` with the IDs of the channels and roles allowed to use the bot.

---

### **Step 4: Save the Code**
Save the code to a file, for example, `discord_vps_deployer.py`.

---

### **Step 5: Run the Bot**
Run the bot using the following command:
```bash
python3 discord_vps_deployer.py
```

---

### **Step 6: Invite the Bot to Your Server**
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Select your application and go to the "OAuth2" tab.
3. Under "OAuth2 URL Generator," select the `bot` scope and the necessary permissions (e.g., `Send Messages`, `Manage Messages`).
4. Copy the generated URL and open it in your browser to invite the bot to your server.

---

### **Step 7: Use the Bot**
1. **Deploy a VPS**:
   Use the `/deploy` command in an allowed channel. For example:
   ```
   /deploy ubuntu 2048 2 60
   ```
   - This deploys a fake VPS with Ubuntu, 2048MB RAM, 2 CPU cores, and a duration of 60 minutes.
   - The bot will send you a tmate SSH session link via DM.

2. **Check VPS Status**:
   Use the `/status` command to check the status of a VPS. For example:
   ```
   /status 1
   ```

3. **Automatic Cleanup**:
   The VPS will be automatically deleted after the specified duration (in minutes).

---

### **Troubleshooting**
1. **Bot Not Responding**:
   - Ensure the bot has the correct permissions in the server.
   - Check that the bot is running and there are no errors in the terminal.

2. **tmate Not Working**:
   - Ensure `tmate` is installed and accessible in your system's PATH.
   - If you're running the bot in a restricted environment (e.g., Docker), ensure `tmate` is installed in the container.

3. **Permissions Issues**:
   - Ensure the bot has the `Send Messages` and `Manage Messages` permissions in the Discord server.
   - Ensure the user running the bot has the necessary permissions to execute commands.

---

Let me know if you encounter any issues!
