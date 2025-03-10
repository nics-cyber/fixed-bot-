import os
import subprocess
import asyncio
import discord
from discord.ext import commands

# Configuration
ALLOWED_CHANNEL_IDS = [123456789012345678]  # Replace with your allowed channel IDs
ALLOWED_ROLE_IDS = [987654321098765432]     # Replace with your allowed role IDs
TOKEN = "YOUR_DISCORD_BOT_TOKEN"            # Replace with your Discord bot token

# Supported OS options (40 operating systems)
SUPPORTED_OS = {
    "ubuntu": "Ubuntu 22.04",
    "debian": "Debian 12",
    "centos": "CentOS 7",
    "fedora": "Fedora 38",
    "arch": "Arch Linux",
    "alpine": "Alpine Linux",
    "kali": "Kali Linux",
    "opensuse": "openSUSE Leap 15.5",
    "rocky": "Rocky Linux 9",
    "freebsd": "FreeBSD 13.2",
    "gentoo": "Gentoo Linux",
    "manjaro": "Manjaro Linux",
    "mint": "Linux Mint 21.2",
    "popos": "Pop!_OS 22.04",
    "zorin": "Zorin OS 16",
    "elementary": "elementary OS 7",
    "deepin": "Deepin 23",
    "mxlinux": "MX Linux",
    "slackware": "Slackware 15",
    "void": "Void Linux",
    "nixos": "NixOS 23.05",
    "clear": "Clear Linux",
    "tails": "Tails",
    "parrot": "Parrot OS",
    "blackarch": "BlackArch Linux",
    "qubes": "Qubes OS",
    "reactos": "ReactOS",
    "haiku": "Haiku OS",
    "solus": "Solus 4.4",
    "puppy": "Puppy Linux",
    "tinycore": "Tiny Core Linux",
    "antix": "antiX Linux",
    "bodhi": "Bodhi Linux",
    "peppermint": "Peppermint OS",
    "lubuntu": "Lubuntu 22.04",
    "kubuntu": "Kubuntu 22.04",
    "xubuntu": "Xubuntu 22.04",
    "ubuntu-budgie": "Ubuntu Budgie 22.04",
    "ubuntu-mate": "Ubuntu MATE 22.04",
    "ubuntu-studio": "Ubuntu Studio 22.04",
    "edubuntu": "Edubuntu 22.04",
    "kali-live": "Kali Linux Live",
    "kali-light": "Kali Linux Light",
    "kali-everything": "Kali Linux Everything",
}

# Track VPS instances
vps_instances = {}

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

def generate_tmate_session():
    """
    Function to generate a tmate SSH session.
    Returns the SSH connection string.
    """
    print("Generating tmate session...")
    # Install tmate if not already installed
    if not os.path.exists("/usr/bin/tmate"):
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "tmate"], check=True)

    # Start tmate and get the SSH connection string
    subprocess.run(["tmate", "-S", "/tmp/tmate.sock", "new-session", "-d"], check=True)
    subprocess.run(["tmate", "-S", "/tmp/tmate.sock", "wait", "tmate-ready"], check=True)
    result = subprocess.run(["tmate", "-S", "/tmp/tmate.sock", "display", "-p", "#{tmate_ssh}"], capture_output=True, text=True, check=True)
    ssh_connection = result.stdout.strip()
    return ssh_connection

def create_vps(os_name: str, ram: int, cpu: int, duration_minutes: int):
    """
    Function to create a fake VPS with the specified OS, RAM, CPU, and duration.
    """
    print(f"Creating fake VPS with OS: {os_name}, RAM: {ram}MB, CPU: {cpu} cores, Duration: {duration_minutes} minutes")
    return {"os": os_name, "ram": ram, "cpu": cpu, "duration_minutes": duration_minutes}

async def cleanup_vps(vps_id: int, timeout_minutes: int):
    """
    Function to automatically delete a fake VPS after a specified timeout in minutes.
    """
    await asyncio.sleep(timeout_minutes * 60)  # Convert minutes to seconds
    if vps_id in vps_instances:
        del vps_instances[vps_id]
        print(f"Fake VPS {vps_id} has been deleted after {timeout_minutes} minutes.")

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.command(name="deploy")
async def deploy_vps(ctx, os_name: str, ram: int, cpu: int, duration_minutes: int):
    """
    Discord command to deploy a fake VPS.
    Only allowed in specific channels and for specific roles.
    """
    # Check if the command is used in an allowed channel
    if ctx.channel.id not in ALLOWED_CHANNEL_IDS:
        await ctx.send("❌ This command is not allowed in this channel.")
        return

    # Check if the user has an allowed role
    if not any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles):
        await ctx.send("❌ You do not have permission to use this command.")
        return

    # Validate OS
    if os_name not in SUPPORTED_OS:
        await ctx.send(f"❌ Unsupported OS. Available options: {', '.join(SUPPORTED_OS.keys())}")
        return

    # Validate RAM and CPU
    if ram < 512 or ram > 16384:
        await ctx.send("❌ Invalid RAM amount. Please specify a value between 512 and 16384 MB.")
        return
    if cpu < 1 or cpu > 16:
        await ctx.send("❌ Invalid CPU count. Please specify a value between 1 and 16 cores.")
        return

    # Validate duration
    if duration_minutes < 1 or duration_minutes > 1440:  # Max 24 hours (1440 minutes)
        await ctx.send("❌ Invalid duration. Please specify a value between 1 and 1440 minutes.")
        return

    # Deploy the fake VPS
    await ctx.send(f"🚀 Deploying fake VPS with OS: {os_name}, RAM: {ram}MB, CPU: {cpu} cores, Duration: {duration_minutes} minutes...")
    try:
        vps = create_vps(os_name, ram, cpu, duration_minutes)
        vps_id = len(vps_instances) + 1
        vps_instances[vps_id] = vps
        await ctx.send(f"✅ Fake VPS deployed successfully! VPS ID: {vps_id}")

        # Generate tmate SSH session
        ssh_connection = generate_tmate_session()
        await ctx.author.send(f"🔑 Your tmate SSH connection for VPS {vps_id}:\n```{ssh_connection}```")
        await ctx.send("📩 Check your DMs for the tmate SSH connection details!")

        # Schedule cleanup after the specified duration
        asyncio.create_task(cleanup_vps(vps_id, duration_minutes))
        await ctx.send(f"⏳ Fake VPS {vps_id} will be deleted in {duration_minutes} minutes.")
    except Exception as e:
        await ctx.send(f"❌ Failed to deploy fake VPS: {e}")

@bot.command(name="status")
async def vps_status(ctx, vps_id: int):
    """
    Discord command to check the status of a fake VPS.
    """
    if vps_id not in vps_instances:
        await ctx.send(f"❌ Fake VPS {vps_id} not found.")
        return

    vps = vps_instances[vps_id]
    await ctx.send(f"✅ Fake VPS {vps_id} is running with OS: {vps['os']}, RAM: {vps['ram']}MB, CPU: {vps['cpu']} cores, Duration: {vps['duration_minutes']} minutes.")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
