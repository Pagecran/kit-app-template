# Procédure 6 Étapes - Farm Job Testing

## Procédure complète pour tester une job definition Farm

### Étape 1: Stop and clean Farm
```bash
powershell -File "D:\NVIDIA-Omniverse\kit-app-template\stop_and_clean_farm.ps1"
```

### Étape 2: Modify files
- Modifier le fichier `hello-world.kit` si nécessaire
- Modifier le fichier `task_hello_world.json` si nécessaire

### Étape 3: Restart Farm
```bash
farm
```
### Étape 4: Upload job definition
```bash
python job_definition_upload.py hello-world.kit --farm-url http://localhost:8222 --api-key change-me
```

### Étape 5: Verify job definition loaded
```bash
curl -s http://localhost:8222/queue/management/jobs/load
```

### Étape 6: Submit task

```bash
curl -X POST "http://localhost:8222/queue/management/tasks/submit" -H "Content-Type: application/json" -d @task_hello_world.json
```

#### Check task status:
```bash
curl -s http://localhost:8222/queue/management/tasks/info/{task_id}
```

#### Check task logs:
```bash
curl -s http://localhost:8222/queue/management/logs/{task_id}?latest_only=true
```




## Règles

1. **Toujours suivre les 6 étapes dans l'ordre**
2. **Remplacer `{task_id}` par l'ID retourné à l'étape 6**
3. **Ne pas inventer de syntaxe, suivre les exemples exactement**
