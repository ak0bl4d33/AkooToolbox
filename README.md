# 📦 AkooToolbox – Blender Addon

 
> **Author:** ak0bl4d3  
> **Blender:** 4.5.3+   

**AkooToolbox** is a Blender addon designed to simplify workflows with **Shape Keys/Surface Deform**, **Vertex Groups**, and **Viewport Display settings**.  
All user settings can be saved and restored when reopening Blender.
Presets can be created for repetitive work

**:moyai: This is a ToolBox. This Tool does not do anything new or better, it only simplifies build-in functions of blender and saves a few clicks c:**

:hammer: Made with help of ChatGPT and VSCode + Build-in Copilot Agent

---

## 🚀 Installation
1. Download `AkooToolBox.py`.  
2. In Blender: **Edit → Preferences → Add-ons → Install...**  
3. Select the file and enable it.  
4. The addon will appear in the **3D View → Sidebar → AkooToolbox**.

---

## ⚙️ Features

### 🔑 Shape Key Tools
- **Surface Deform with Shapes**  
  - Transfers Shape Keys from a source object to the active (target) object.  
  - Supports *Include* and *Exclude* filters.  
  - **Important:** Lists must be **comma-separated** (e.g., `ButtBig, ButtSmall, ThighBig`).  

- **Paste locked Shape Keys**
  - Pastes every locked Shape Key into the Include/Exclude textbox.

- **Remove Empty Shape Keys**  
  - Removes Shape Keys that have no delta from the Basis.  

- **Reset Settings**  
  - Resets falloff and strength values to their defaults.  

---

### 🧩 Vertex Group Tools
- **Transfer Vertex Groups**  
  - Transfers selected Vertex Groups using the **Data Transfer Modifier**.  
  - Supports *Include* and *Exclude* filters.  
  - **Important:** Lists must be **comma-separated** (e.g., `Hip, Spine, Chest`).  

- **Paste locked Vertex Groups**
  - Pastes every locked Vertex Group into the Include/Exclude textbox.

  - Mapping methods available:  
    `TOPOLOGY`, `NEAREST`, `EDGE_NEAREST`, `POLYINTERP_NEAREST`, and more.  

- **Weight Paint Smoothing**  
  - Smooths weight paint data on Vertex Groups.  
  - Iterations can be customized (default: `2`).  
  - **Tip:** Use Include/Exclude to avoid smoothing *all* vertex groups.  

---

### 👁️ Viewport Display Tools
- **Fix Viewport Display**  
  - Forces Armature display settings in the viewport.  
  - **Options** (must be **comma-separated**):  
    - Flags: `show_name`, `show_axis`, `show_in_front`  
    - Display types: `wire`, `solid`, `textured`, `bounds`  
    - Bound types: `box`, `sphere`, `cylinder`, `cone`, `capsule`  
- Example:**  
  - `show_in_front, wire, box`
- **Important:** this is case sensitive and everything must be lower case. This example ( `Show_In_Front, WIRE, bOX`) will not work.
---

### 💾 Save Settings
- The **Save Settings** button stores the last used values into a JSON file:  
`%APPDATA%\Blender Foundation\Blender<Version>\config\AkooToolbox_config.json`

---
### 💾 Save/Load/Delete Presets
- Presets store every current value in textboxes into a JSON file:  
`%APPDATA%\Blender Foundation\Blender<Version>\config\AkooToolbox_presets.json`


- Whats Saved?
  - surface_deform
    - `falloff`, `strength`, `include_exclude_textfield`
  - vertex_group
    - `mix_mode`, `mix_set`, `mix_normalize`, `mix_default_a`, `mix_default_b`, `mapping_method`, `smoothing_amount`, `include_exclude_textfield`
  - viewportdisplay
    - `settings`

---

## 📝 Notes
- :warning:**Source and Target objects cannot be the same.**
- If a Shape Key already exists on the target, it will be skipped.  
- If no *Include* list is set → **all Shape Keys/Groups will be used.**  
- If *Exclude* list is set → **those will be ignored.**  
- All lists must be **comma-separated**.

---

## 📋 Example Workflows

**Transfer Shape Keys (only ButtBig & ButtSmall, exclude ThighBig):**
Include: `ButtBig`, `ButtSmall`
Exclude: `ThighBig`

**Smooth Vertex Groups (Spine & Chest only, 5 iterations):**
Include: `Spine`, `Chest`
Iterations: `5`

**Fix Viewport Display:**
`show_in_front`, `show_name`, `wire`, `sphere`

---

## 🛠️ Developer Info
- The addon saves and loads settings via JSON config.  
- UI is structured into collapsible **Regions**:  
  - Source Mesh  
  - Shape Keys  
  - Vertex Groups  
  - Viewport Display  
  - Save/Load

---

