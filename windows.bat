py -3 -m venv .
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& './Scripts/activate'"
python -m pip install --upgrade pip
pip install discord.py[voice]
pip install python-dotenv
