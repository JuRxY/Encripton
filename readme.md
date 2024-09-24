<p align="center">
    <img align="center" src="./assets/icon.png" height="180px">
</p>

<h1 align="center">Enkrypton</h1>
<h3 align="center">An open source encription and compression GUI.</h3>
<br>

## Requirements
![][python-shield]

## Install
The pre-built version for windows is available:
```bash
git clone https://github.com/JuRxY/Enkrypton.git
cd Enkrypton/bin
./Enkrypton-win.exe
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
pyinstaller --noconfirm --onefile --windowed --icon "./assets/icon.ico" --add-data "./assets/dragndrop.png;assets"  "./ui.py"
```

[python-shield]: https://img.shields.io/badge/Python-3.5^-green?style=for-the-badge&logo=python