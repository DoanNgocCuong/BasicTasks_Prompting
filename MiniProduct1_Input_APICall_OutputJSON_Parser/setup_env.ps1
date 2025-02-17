Write-Host "Creating virtual environment..."
python -m venv .venv

Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Setup completed!" 