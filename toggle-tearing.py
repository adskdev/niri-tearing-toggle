#!/usr/bin/env python3
import json
import subprocess
import os
import argparse

START_MARKER = "// --- AUTO-TEARING START ---"
END_MARKER = "// --- AUTO-TEARING END ---"

def send_notification(title, message, icon="video-display"):
    """Helper function to send desktop notifications."""
    subprocess.run(['notify-send', '-a', 'Niri', '-i', icon, title, message])

def main():
    parser = argparse.ArgumentParser(description="Toggle screen tearing for the focused Niri window.")
    parser.add_argument("-c", "--config", 
                        default="~/.config/niri/config.kdl", 
                        help="Path to the Niri config file to modify (default: ~/.config/niri/config.kdl)")
    args = parser.parse_args()
    
    config_file = os.path.expanduser(args.config)

    # Get the focused window data from Niri IPC
    try:
        res = subprocess.run(['niri', 'msg', '-j', 'focused-window'], capture_output=True, text=True, check=True)
        window_data = json.loads(res.stdout)
        
        # Check for both snake_case and kebab-case variants
        app_id = window_data.get("app_id") or window_data.get("app-id")
        
    except Exception as e:
        send_notification("IPC Error", f"Failed to communicate with Niri:\n{e}", "dialog-error")
        return

    # Fallback to display raw output for debugging if app-id is missing
    if not app_id:
        debug_info = ", ".join(window_data.keys()) if isinstance(window_data, dict) else str(window_data)
        send_notification("Error", f"App-ID not found for this window!\nAvailable fields: {debug_info}", "dialog-error")
        return

    # Read the current configuration file
    if not os.path.exists(config_file):
        send_notification("Configuration Error", f"Config file not found:\n{config_file}", "dialog-error")
        return

    with open(config_file, "r") as f:
        lines = f.readlines()

    before_block, after_block = [], []
    managed_apps = set()
    state = 0  # 0 = before marker, 1 = inside block, 2 = after block

    for line in lines:
        if line.strip() == START_MARKER:
            state = 1
            continue
        elif line.strip() == END_MARKER:
            state = 2
            continue

        if state == 0:
            before_block.append(line)
        elif state == 1:
            if "match app-id=" in line:
                # Extract the app-id, cleaning up regex anchors (^ and $)
                parts = line.split('"')
                if len(parts) >= 3:
                    managed_apps.add(parts[1].strip('^$'))
        elif state == 2:
            after_block.append(line)

    # Toggle tearing state for the current app-id
    if app_id in managed_apps:
        managed_apps.remove(app_id)
        msg = f"Tearing DISABLED\nWindow: {app_id}"
    else:
        managed_apps.add(app_id)
        msg = f"Tearing ENABLED\nWindow: {app_id}"

    # Rebuild the configuration content
    new_content = "".join(before_block)
    if new_content and not new_content.endswith("\n"):
        new_content += "\n"

    if managed_apps:
        new_content += f"{START_MARKER}\n"
        for app in managed_apps:
            new_content += f"window-rule {{\n    match app-id=\"^{app}$\" is-focused=true\n    allow-tearing true\n}}\n"
        new_content += f"{END_MARKER}\n"

    new_content += "".join(after_block)

    # Save the file and trigger a Niri config reload
    with open(config_file, "w") as f:
        f.write(new_content)

    subprocess.run(['niri', 'msg', 'action', 'read-config'])
    send_notification("Screen Tearing", msg)

if __name__ == "__main__":
    main()