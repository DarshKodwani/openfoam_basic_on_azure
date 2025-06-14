#!/bin/bash

echo "🔄 Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "🔑 Adding OpenFOAM repository key..."
sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"

echo "➕ Adding OpenFOAM repository..."
sudo add-apt-repository http://dl.openfoam.org/ubuntu
sudo apt update

echo "📦 Installing OpenFOAM and ParaView..."
sudo apt install -y openfoam10 paraviewopenfoam510

echo "🔧 Configuring OpenFOAM environment..."
if ! grep -Fxq "source /opt/openfoam10/etc/bashrc" ~/.bashrc
then
  echo "source /opt/openfoam10/etc/bashrc" >> ~/.bashrc
fi

echo "📌 Sourcing OpenFOAM environment for current session..."
source /opt/openfoam10/etc/bashrc

echo "✅ Done. You can now run OpenFOAM commands like 'blockMesh' and 'simpleFoam'."
