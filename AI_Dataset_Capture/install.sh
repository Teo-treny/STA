#!/bin/bash

# === Config ===
SERVICE_NAME=teleop
SCRIPT_PATH="/home/pi/Desktop/Teleop/app.py"
WORK_DIR="/home/pi/Desktop/Teleop"
USER_NAME="pi"
VENV_PATH="$WORK_DIR/venv"
PYTHON_BIN="$VENV_PATH/bin/python"

# === Vérifications ===
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Erreur : Script Python introuvable à $SCRIPT_PATH"
    exit 1
fi

if [ ! -f "$PYTHON_BIN" ]; then
    echo "❌ Erreur : Environnement virtuel introuvable à $PYTHON_BIN"
    echo "💡 Crée-le avec : python3 -m venv $VENV_PATH"
    exit 1
fi

# === Création du fichier systemd ===
echo "📄 Création du service systemd..."
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Flask Teleop Robot App
After=network.target

[Service]
ExecStart=$PYTHON_BIN $SCRIPT_PATH
WorkingDirectory=$WORK_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$USER_NAME
Environment=FLASK_ENV=production
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# === Activation et démarrage ===
echo "🚀 Activation du service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service
sudo systemctl restart $SERVICE_NAME.service

echo "✅ Service '$SERVICE_NAME' installé et redémarré."
echo "ℹ️  Vérifie avec : sudo systemctl status $SERVICE_NAME"
