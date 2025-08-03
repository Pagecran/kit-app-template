# Guide NVIDIA Omniverse Farm Standalone - Windows Local

Ce guide documente la configuration d'un système de render queue local avec NVIDIA Omniverse Farm Standalone 2.0.42 sur Windows.

> **Note d'évolution :** Ce guide pourra être adapté pour un déploiement Farm Linux centralisé ultérieurement.

## Prérequis

- **Windows 10 ou plus récent**
- **Python 3.10 ou ultérieur** (obligatoire pour Farm 2.0.42)
- **NVIDIA Omniverse Kit App Template** installé
- **GPU NVIDIA** pour le rendu

## 1. Installation Farm Standalone

### 1.1 Téléchargement
- Télécharger **Farm 2.0 Standalone** depuis NGC Resource (NVIDIA GPU Cloud)
- Décompresser le package Windows dans un répertoire local

### 1.2 Installation Python
```bash
# Naviguer vers le dossier des dépendances
cd farm_standalone_2.0.42/_/windows/dependencies/

# Installer Farm et toutes ses dépendances
python3 -m pip install --find-links dependencies nv_svc_farm-2.0.42-py3-none-any.whl

# Vérification
python3 -c "import nv.svc.farm; print('Farm installé avec succès')"
```

### 1.3 Configuration PATH (Windows)
Ajouter le répertoire des scripts Python au PATH utilisateur :
```powershell
# PowerShell - Ajouter Python Scripts au PATH
$userpath = [System.Environment]::GetEnvironmentVariable('PATH','USER')
$userpath = $userpath + ';C:\Users\USERNAME\AppData\Local\Programs\Python\Python310\Scripts'
[System.Environment]::SetEnvironmentVariable('PATH',$userpath,'USER')

# Redémarrer le terminal pour appliquer les changements
```

## 2. Configuration et lancement

### 2.1 Fichier de configuration (optionnel)
Créer `farm_config.toml` pour personnaliser les paramètres :
```toml
[settings.nv.svc.server.http]
host = "localhost"
port = "8222"
```

### 2.2 Lancement Farm
```bash
# Option 1 : Lancement simple (Queue + Agent local)
farm

# Option 2 : Avec fichier de configuration
farm --config farm_config.toml

# Option 3 : Queue seulement (pour setup distribué futur)
farm-api --config farm_config.toml
```

### 2.3 Vérification
```bash
# Test de statut
curl http://localhost:8222/status

# Interface Dashboard
# Ouvrir : http://localhost:8222/queue/management/dashboard
```

**Important :** Farm peut automatiquement changer de port si celui configuré est occupé (ex: 8222 → 8025).

## 3. Job Definition pour Kit Rendering

### 3.1 Localisation
Les job definitions sont stockées dans :
```
Windows: %LOCALAPPDATA%/nvidia/nv-svc-farm/job-definitions/
```

### 3.2 Job Definition fonctionnelle
Créer le fichier `job.omni.farm.render.kit` :
```toml
[package]
authors = ["Kit Team"]
category = "farm-jobs"
description = "Omniverse Agent Render Job"
title = "Omniverse Agent Render Job"
version = "0.1.0"
keywords = ["job"]

[dependencies]
"omni.services.render" = {}
"omni.services.farm.agent.runner" = {}
"omni.services.transport.client.http_async" = { version = "1.3.1"}

[job.create-render]
job_type = "kit-service"
name = "create-render"

# CRUCIAL : Appeler kit.exe directement, PAS le .bat
command = 'C:\\chemin\\vers\\kit\\kit.exe'

args = [
    "C:\\chemin\\vers\\apps\\votre_app.kit",
    "--enable omni.services.render"
]

task_function = "render.run"
headless = true
env = {}
log_to_stdout = true
```

**Points critiques :**
- Utiliser `kit.exe` directement, jamais les fichiers `.bat`
- Chemins absolus avec simple quotes
- Double backslashes `\\` dans les chemins Windows

## 4. Configuration USD Composer

### 4.1 Configuration Movie Capture
Dans le fichier `.kit` de votre application :
```toml
[settings.exts."omni.kit.window.movie_capture"]
enabled = true
availableFarms = [
    { name = "localhost queue", url = "http://localhost:8222" }
]
```

**Important :** Adapter le port selon celui effectivement utilisé par Farm.

### 4.2 Lancement USD Composer
```bash
# Syntaxe correcte bash pour Windows .bat
cmd //c "chemin\\vers\\votre_app.kit.bat"
```

## 5. Architecture du système local

```
USD Composer
    ↓ Movie Capture HTTP
Farm Queue (localhost:8222)
    ↓ Job Dispatch
Farm Agent (local)
    ↓ Process Launch
Kit.exe + Render Service
    ↓ Output
Images rendues
```

## 6. Validation du setup

### 6.1 Tests de base
```bash
# 1. Statut des services
curl http://localhost:8222/status

# 2. Job definitions chargées
curl http://localhost:8222/queue/management/jobs/load

# 3. Dashboard web
# Ouvrir : http://localhost:8222/queue/management/dashboard
```

### 6.2 Test de rendu simple
1. Créer une scène USD basique avec une sphère
2. Utiliser Movie Capture pour rendre 1 frame
3. Vérifier les logs Farm pour `return code: 0`
4. Localiser l'image de sortie

### 6.3 Sources de logs
- **Farm :** Logs console + fichier log si configuré
- **Kit :** `%LOCALAPPDATA%/ov/data/Kit/[APP]/logs/`
- **Tasks Farm :** API `/queue/management/logs/{task_id}`

## 7. Dépannage erreurs courantes

| Erreur | Cause | Solution |
|--------|-------|----------|
| `return code: 126` | .bat non exécutable par Farm | Utiliser `kit.exe` directement |
| `'arb.scripting-python.plugin' not found` | Parsing arguments .bat | Éviter les .bat |
| `/c: Is a directory` | Mauvaise syntaxe cmd | Syntaxe correcte ou éviter cmd |
| `farm: command not found` | PATH mal configuré | Ajouter Python Scripts au PATH |
| `UnicodeDecodeError` | Encoding messages Windows | Ajouter `PYTHONIOENCODING=utf-8` |

## 8. Syntaxes spécifiques Windows

### 8.1 Bash (Claude Code)
```bash
# Lancer .bat
cmd //c "chemin\\fichier.bat"

# Lancer .exe  
"chemin\\fichier.exe" args

# Toujours : \\ pour chemins, // pour options cmd
```

### 8.2 PowerShell variables
```powershell
# Lire
$var = [System.Environment]::GetEnvironmentVariable('PATH','USER')

# Écrire
[System.Environment]::SetEnvironmentVariable('PATH',$newvalue,'USER')
```

## 9. Optimisations recommandées

### 9.1 Job Definition optimisée
```toml
args = [
    "chemin\\vers\\app.kit",
    "--enable omni.services.render",
    "--no-window",
    "--/app/file/ignoreUnsavedOnExit=true",
    "--/app/hangDetector/enabled=false",
    "--/app/asyncRendering=false"
]

env = {
    "PYTHONIOENCODING" = "utf-8"
}
```

### 9.2 Configuration Farm robuste
```toml
# Dans farm_config.toml
[settings.nv.svc.jobs]
task_timeout = 300
retry_count = 1

[settings.nv.svc.controller]
checkin_timeout = 60
max_concurrent_tasks = 1
```

## 10. Évolution vers setup distribué

**Préparation pour Farm Linux centralisé :**
- Utiliser `farm-api` pour Queue centralisé
- Configurer `controller-svc` sur agents Windows
- Adapter la configuration réseau
- Gérer l'authentification et sécurité
- Synchroniser les job definitions

**Points d'attention :**
- Chemins réseau pour assets USD
- Gestion des outputs distribués  
- Monitoring centralisé
- Load balancing des tâches

## Résumé points critiques

✅ **Configurations qui marchent :**
- Python 3.10+ obligatoire
- `kit.exe` directement (pas .bat)
- Chemins absolus avec `\\`
- Syntaxe bash : `cmd //c` 

❌ **Pièges à éviter :**
- Utiliser les fichiers .bat dans job definitions
- Oublier les doubles backslashes
- PATH système/utilisateur mal configuré
- Ports hardcodés (Farm peut changer automatiquement)