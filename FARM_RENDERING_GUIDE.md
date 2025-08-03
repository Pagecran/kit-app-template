# NVIDIA Omniverse Farm - Kit Rendering Guide

## Kit Arguments de Rendu (Arguments de Ligne de Commande)

### Arguments Officiels pour Rendu avec Kit
D'après la documentation officielle, voici les arguments Kit pour activer le rendu :

```bash
--enable omni.services.render
--/app/file/ignoreUnsavedOnExit=true
--/app/extensions/excluded/0=omni.kit.window.privacy
--/app/hangDetector/enabled=0
--/app/asyncRendering=false
--/rtx/materialDb/syncLoads=true
--/omni.kit.plugin/syncUsdLoads=true
--/rtx/hydra/materialSyncLoads=true
--/rtx-transient/resourcemanager/texturestreaming/async=false
--/rtx-transient/resourcemanager/enableTextureStreaming=false
--/exts/omni.kit.window.viewport/blockingGetViewportDrawable=true
--/rtx-transient/dlssg/enabled=false
```

### Syntaxe des Arguments
- **Espaces**: `--enable omni.services.render` (PAS `--enable=omni.services.render`)
- **Paths settings**: `--/app/hangDetector/enabled=0`
- **Extensions**: `--/exts/omni.kit.window.viewport/blockingGetViewportDrawable=true`

## Structure des Job Definitions (.kit files)

### Job Definition de Base (job_type = "base")
```toml
[job.hello-world]
job_type = "base"
name = "hello-world"
command = "python"
args = ["-c", "print('Hello World!')"]
log_to_stdout = true
```

### Job Definition Kit Service (job_type = "kit-service")
```toml
[job.create-render]
job_type = "kit-service"
name = "create-render"
command = 'C:\Program Files\my_app\my_usd_composer.kit.bat'
args = [
    "--enable omni.services.render",
    "--/app/file/ignoreUnsavedOnExit=true",
    "--/app/hangDetector/enabled=0",
    "--/app/asyncRendering=false",
    "--/rtx/materialDb/syncLoads=true",
    "--/omni.kit.plugin/syncUsdLoads=true",
    "--/rtx/hydra/materialSyncLoads=true"
]
task_function = "render.run"
headless = true
env = {}
log_to_stdout = true
```

### Propriétés des Job Definitions
- `name`: Identifiant convivial du job
- `command`: Exécutable à lancer
- `args`: Arguments pour la commande
- `log_to_stdout`: Capturer les logs du job
- `env`: Variables d'environnement
- `allowed_args`: Arguments configurables du job
- `headless`: Mode d'exécution (pour kit-service)
- `task_function`: Point d'entrée du service (pour kit-service)

## Types de Tasks

### Task de Base
```json
{
   "user": "Username",
   "task_type": "hello-world",
   "task_args": {},
   "status": "submitted"
}
```

### Task avec Arguments
```json
{
   "task_type": "create-render",
   "task_function": "render.run",
   "user": "test-user",
   "task_args": {
       "usd_file": "path/to/scene.usd",
       "render_settings": {
           "output_folder": "C:/temp/render_output",
           "start_frame": 1,
           "end_frame": 10,
           "res_width": 1920,
           "res_height": 1080,
           "file_name": "render",
           "file_extension": "png"
       }
   }
}
```

## API omni.services.render

### Endpoint Principal
- **URL**: `/run`
- **Méthode**: POST
- **Description**: "Render the given USD stage using the provided options"

### Paramètres de Rendu (RenderSettings)
```python
{
    "usd_file": "path/to/scene.usd",
    "render_start_delay": 10,
    "render_stage_load_timeout": 0,
    "render_settings": {
        "output_folder": "C:/temp/output",
        "file_name": "render",
        "file_name_num_pattern": ".####",
        "file_type": ".png",
        "res_width": 1920,
        "res_height": 1080,
        "start_frame": 1,
        "end_frame": 48,
        "fps": 24.0,
        "camera": "camera",
        "render_preset": 0,  # PATH_TRACE=0, RAY_TRACE=1, IRAY=2
        "spp_per_iteration": 1,
        "path_trace_spp": 64
    }
}
```

## Commandes d'Application Kit

### Windows
```bash
# USD Composer
"C:\Program Files\omniverse\composer\omni.usd_composer.kit.bat"

# Kit Direct
"C:\Path\To\kit\kit.exe" "C:\Path\To\app.kit"
```

### Linux
```bash
# USD Composer
"/opt/omniverse/composer/omni.usd_composer.kit.sh"

# Kit Direct
"/path/to/kit/kit" "/path/to/app.kit"
```

## Évolution Graduelle : Hello World → Rendu

### Étape 1 : Hello World de Base
```toml
[job.hello-world]
job_type = "base"
name = "hello-world" 
command = "python"
args = ["-c", "print('Hello World!')"]
log_to_stdout = true
```

### Étape 2 : Appel Kit Simple
```toml
[job.hello-world]
job_type = "base"
name = "hello-world"
command = "D:\\Path\\To\\kit\\kit.exe"
args = ["--quit"]
log_to_stdout = true
```

### Étape 3 : Kit avec Service Render
```toml
[job.hello-world]
job_type = "base" 
name = "hello-world"
command = "D:\\Path\\To\\kit\\kit.exe"
args = ["--enable omni.services.render", "--quit"]
log_to_stdout = true
```

### Étape 4 : Ouverture de Scène USD
```toml
[job.hello-world]
job_type = "base"
name = "hello-world"
command = "D:\\Path\\To\\kit\\kit.exe"
args = [
    "--enable omni.services.render",
    "--open D:\\Path\\To\\scene.usd",
    "--quit"
]
log_to_stdout = true
```

### Étape 5 : Ajout d'Arguments de Rendu
```toml
[job.hello-world]
job_type = "base"
name = "hello-world"
command = "D:\\Path\\To\\kit\\kit.exe"
args = [
    "--enable omni.services.render",
    "--open D:\\Path\\To\\scene.usd",
    "--/app/asyncRendering=false",
    "--/rtx/materialDb/syncLoads=true",
    "--quit"
]
log_to_stdout = true
```

## RÈGLES IMPORTANTES

### Syntaxe des Arguments
1. **PAS de `=` pour les extensions** : `--enable omni.services.render`
2. **`=` pour les settings paths** : `--/app/hangDetector/enabled=0`
3. **Guillemets simples pour les paths Windows** : `command = 'C:\Program Files\app.bat'`
4. **Un argument par élément du tableau** : `["--enable omni.services.render", "--quit"]`

### Processus de Modification Graduelle
1. **UNE modification à la fois**
2. **Tester après chaque modification**
3. **Revenir en arrière si ça ne marche pas**
4. **Suivre les exemples officiels EXACTEMENT**
5. **Ne PAS inventer de syntaxe**

### Chemins et Accès
- **Agents doivent avoir accès au GPU NVIDIA**
- **Agents doivent accéder aux fichiers USD**
- **Agents doivent accéder à l'application Kit**
- **Vérifier les paths absolus**

## Notes de Débogage

### Vérifications de Base
1. Farm Queue accessible : `http://localhost:8222/health`
2. Agents actifs : `GET /queue/management/agents/list`
3. Job definitions chargées : `GET /queue/management/jobs/load`
4. Tasks soumises : `POST /queue/management/tasks/submit`

### Problèmes Courants
- **task_types vides** : Redémarrer Farm complètement
- **Agents ne prennent pas les tâches** : Vérifier task_types des agents
- **Authentification** : API `/jobs/save` nécessite x-api-key
- **Chemins Windows** : Utiliser `\\` ou `/` selon le contexte