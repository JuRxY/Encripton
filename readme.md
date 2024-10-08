<p align="center">
    <img align="center" src="./assets/icon.png" height="180px">
</p>

<h1 align="center">Enkrypton</h1>
<h3 align="center">An open source encription and compression GUI.</h3>
<hr>

<p align="center">
    <img align="center" src="./assets/sshot1.png">
</p>

## Requirements
![][python-shield]

## Install
The pre-built version for windows is available for download in the releases or you can download it with the following command in Windows Powershell:
```bash
Invoke-WebRequest -Uri "https://github.com/JuRxY/Enkrypton/releases/download/v1.0/Enkrypton.exe" -OutFile "Enkrypton.exe"
```

## Run with python (modify)

Clone the directory
```bash
git clone https://github.com/JuRxY/Enkrypton.git
cd Enkrypton
```
Install dependencies and run
```bash
pip install -r requirements.txt
python ui.py
```
Build executable (optional)
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --icon "./assets/icon.ico" --name "Enkrypton" --add-data "./assets/dragndrop.png;assets" --add-data "./assets/icon.ico;assets" --add-data "./endecryption.py;."  "./ui.py"
```
Your executable will be generated at `./dist/Enkrypton.exe`

[python-shield]: https://img.shields.io/badge/Python-3.5^-green?style=for-the-badge&logo=python
