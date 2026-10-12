# Niri Tearing Toggle
A lightweight, seamless tool to dynamically toggle screen tearing (`allow-tearing`) for the currently focused window in the [Niri](https://github.com/YaLTeR/niri) Wayland compositor.

## Why does this exist?
Wayland compositors handle screen tearing strictly. If you want tearing for games (to reduce input lag), you usually have to hardcode the game's `app_id` into your configuration. 

Furthermore, if you try to toggle tearing using a GUI launcher or a shell script that steals focus, Wayland might misbehave, or the tearing rule will apply to the wrong window. 

**This script solves that.** By binding it to a keyboard shortcut, you can press it *while inside your game*. It fetches the active `app_id` via Niri's IPC, edits a dedicated block in your KDL configuration file, and reloads Niri instantly.

## Prerequisites
* Python 3
* `libnotify` (for `notify-send` desktop notifications)
* A Niri fork/version that supports the `allow-tearing` window rule: https://github.com/urayde/niri

## Installation
1. Clone this repository:
```bash
git clone [https://github.com/adskdev/niri-tearing-toggle.git](https://github.com/adskdev/niri-tearing-toggle.git)
cd niri-tearing-toggle
```

2. Run the installer script:
```bash
./install.sh
```

## Configuration
Add a keybind to your Niri configuration file (usually ~/.config/niri/config.kdl).

#### Default Usage
If your window rules are in the main `config.kdl`:
```
binds {
    // Press Super+Shift+T to toggle tearing for the focused window
    Mod+Shift+T { spawn "niri-tearing-toggle"; }
}
```

#### Custom Config Path
If you split your Niri config and store your rules in a different file (e.g., `~/.config/niri/cfg/rules.kdl`), pass the `-c` flag:
```
binds {
    Mod+Shift+T { spawn "niri-tearing-toggle" "-c" "~/.config/niri/cfg/rules.kdl"; }
}
```

## How it works
The script safely manages a specific block in your config file. It looks for these exact comments:
```
// --- AUTO-TEARING START ---
// --- AUTO-TEARING END ---
```
You don't even need to add these comments yourself! The first time you use the hotkey, the script will automatically append this block to the end of your targeted configuration file.