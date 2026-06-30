<div align="center">
<h1>Storage Hunters Tool</h1>
  <p>The definitive <b>Storage Hunters Macro</b> for <b>Roblox</b></p>
</div>

<div align="center">

[![License](https://img.shields.io/github/license/AlinaWan/bees-tool)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![Visual Studio](https://custom-icon-badges.demolab.com/badge/Visual%20Studio-5C2D91.svg?&logo=visualstudio&logoColor=white)](#)
[![❤︎](https://img.shields.io/badge/Made%20with%20%E2%9D%A4%20by%20Riri-FFCAE9)](#)

</div>

> *“Omnia moventur, unum congruit.”* — Riri, circa 2026

Storage Hunters Tool est instrumentum visionis computatralis ad executionem in tempore reali destinatum, constructum pro ambitu [Storage Hunters: Open World](https://www.roblox.com/games/98800969324557). Systema motum signi per continuum spatium observat et regionem propositam in eodem plano perpendit. Cum motus et regio in congruentiam veniunt, actio statim exercetur.

<div align="center">
  <video src="https://github.com/user-attachments/assets/c65d0a7f-f500-4ed2-a303-71e90aa21e77" width="100%" controls>
  </video>
  <video src="https://github.com/user-attachments/assets/c6efdbc6-c534-4ff3-a288-1b001020fb76" width="100%" controls>
  </video>
</div>

This project is derived from one of my previous macros, [Bees Tool](https://github.com/AlinaWan/bees-tool). The first commit of this project continues from [this](https://github.com/AlinaWan/bees-tool/commit/3fe1410c69087503c06fea75d267cc0d49bc91b9) commit.

Storage Hunters Tool relies on Windows Dynamic Link Libraries (WinDLLs) for core features and is only supported on machines running Windows.

-----

## 📥 Installation

### 📦 Prerequites

- Windows 10 or 11
- Python 3.10 or higher

### 💻 Setup

1. Install **Python dependencies** via Pip:
   ```powershell
   pip install -r requirements.txt
   ```

3.  Initialize the script via terminal:
    ```powershell
    python src\program.pyw
    ```

-----

## ⌨️ Controls

| Keybind                           | Action                                                                           |
| :-------------------------------- | :------------------------------------------------------------------------------- |
| <kbd>F6</kbd>                     | **Toggle State**: Switches the tool between Active (Green) and Standby (Red).    |
| <kbd>F7</kbd>                     | **Toggle Debug**: Toggles the visibility of the detection mask debug window.     |
| <kbd>Shift</kbd> + <kbd>Esc</kbd> | **Termination**: Immediately closes the script and destroys all overlay windows. |
| <kbd>Ctrl</kbd> + <kbd>F10</kbd>  | **Menu Toggle**: Shows or hides the menu for importing, editing, and saving configurations. |

### Telemetry Overlay

The script provides real-time visual feedback via a transparent Tkinter canvas. The **Region of Interest (ROI)** indicators communicate the current state:

* **Green ROI Points**: Tool is **Active/ON**. The system is actively interrogating the search domain.
* **Red ROI Points**: Tool is **Inactive/OFF**. Logic is suspended, though the overlay remains initialized.

## 🛠️ Configuration
Storage Hunters Tool is highly customizable. All profiles and automation behaviors are handled via **Configuration Files** (`.json`). 

> [!TIP]
> For a full breakdown of every constant and how to tune them, please see:
>
> ➔ [CONFIGURATION.md](docs/CONFIGURATION.md)

-----

## 🛰️ Nomenclature & Phonetics

To maintain alignment with the architectural vision of the framework, the designation **Storage Hunters Tool** is to be phonetically rendered as **/ˈstɔːrɪzː/** (*as in "charisma"*).

The voiced postalveolar affricate **/ˈstɔːrɪdʒ/** (as in a space or a place for storing) is considered a lexical deviation and will not be tolerated in formal interrogation or community discourse. Proper sibilance is a prerequisite for tool competency.

Users will find themselves experiencing a profound sense of gratitudo for the privilege of utilizing the (elongated) voiced alveolar fricative. (See: [Bees Tool](https://github.com/AlinaWan/bees-tool#%EF%B8%8F-nomenclature--phonetics))

-----

## 🫶 Acknowledgements

As with most of my macros, Storage Hunters Tool is influenced by [iamnotbobby](https://github.com/iamnotbobby)'s [Dig Tool](https://github.com/iamnotbobby/dig-tool), which I've been a part of in
the past. I feel the need to explicitly acknowledge this project in this specific macro due to Storage Hunters' minigame's glaring resemblance to the one in [DIG](https://www.roblox.com/games/126244816328678).
While all of the code is my own work, I owe some of the architectural choices to my experience with Dig Tool.

-----

## 📝 End Notes

[![Discord Server](https://img.shields.io/discord/1520944787832700968?label=Join%20Riri's%20Discord%20Server!&style=for-the-badge&logo=discord)](https://discord.gg/EFDsph8EJF)

Also See:
 * [Bees Tool](https://github.com/AlinaWan/bees-tool) for [Bees](https://www.roblox.com/games/92528179587394)
 * [Mine Tool](https://github.com/AlinaWan/mine-tool) for [Mine](https://www.roblox.com/games/115694170181074)
 * [iamnotbobby](https://github.com/iamnotbobby)'s [Dig Tool](https://github.com/iamnotbobby/dig-tool) for [DIG](https://www.roblox.com/games/126244816328678)

-----

## 📄 License

Storage Hunters Tool is provided as-is under the [MIT License](LICENSE).

Copyright (c) 2026 Riri
