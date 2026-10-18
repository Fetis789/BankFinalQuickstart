# Quickstart
Ниже приведем последовательность команд, которые нужно проделать для запуска кластера и сервисов у себя на локальном компьютере. В случае отсутствия в вашем окружении каких-либо сервисов в раскрывающихся разделах есть дополнительные команды для их загрузки

## 1. Клонирование репозитория и настройка окружения
git clone https://github.com/Fetis789/BankMarketingPetModel.git .


## 2. Настройка uv
<details>
<summary> Установка uv</summary>

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
```
</details>

### Настройка
```
uv --version
uv python install 3.11
uv sync --locked
uv run python --version
```

## 3. Установка и проверка docker, kind, kubectl, helm, curl

Перед запуском кластера необходимо проверить наличие всех необходимых для этого инструментов. И установить их, если они отсутствуют.

<details>
<summary> Установка всех сервисов</summary>
```powershell
winget install --exact --id Docker.DockerDesktop
winget install --exact --id Kubernetes.kind
winget install --exact --id Kubernetes.kubectl
winget install --exact --id Helm.Helm
winget install --exact --id cURL.cURL
```

```bash
sudo apt-get update
sudo apt-get install -y curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"

ARCH=$(dpkg --print-architecture)
curl -Lo /tmp/kind "https://kind.sigs.k8s.io/dl/v0.33.0/kind-linux-$ARCH"
sudo install /tmp/kind /usr/local/bin/kind
curl -Lo /tmp/kubectl "https://dl.k8s.io/release/v1.37.1/bin/linux/$ARCH/kubectl"
sudo install /tmp/kubectl /usr/local/bin/kubectl
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4 | bash
```
</details>



Проверить наличие сервисов можно следующим списком команд:
```
docker version
docker info
kind version
kubectl version --client
helm version
curl --version
```

Дополнительно к этому перед раскаткой кластера необходимо проверить, что локальный порт 80 свободен, так как Traefik при раскатке кластера будет работать именно на нем. Это можно сделать одной из следующих команд:
<details>
<summary> Команды для проверки порта</summary>

```powershell
Get-NetTCPConnection -LocalPort 80 -State Listen -ErrorAction SilentlyContinue"
```

```bash_windows
netstat -ano | grep ':80 '
```

```bash_linux
sudo ss -ltnp 'sport = :80'
```
</details>

После проверки всех инструментов и занятости порта можно раскатывать кластер.

## 4. Раскатка кластера
Основной процесс раскатки есть в файле up.sh, но перед этим нужно загрузить в docker некоторые используемые образы.

```
docker pull apache/airflow:3.3.2
docker pull ghcr.io/mlflow/mlflow:v3.16.1
docker pull rustfs/rustfs:1.0.0
```

**Важно:** Некоторые из этих образов могут не спуллиться. Это нормально. Их пуллинг прописан отдельно в манифестах в папке /platform, при сборе они дозагрузятся.

Далее запускаем сам файл, в котором делается развертывание кластера. **Крайне важно** - команду запуска лучше писать в **Git Bash**. Перед командой также лучше выполнить обновление helm repo.

```
helm repo update
bash platform/up.sh
```

В результате исполнения файла должен появиться кластер с архитектурой для ML-сервиса. На кластере должны быть MlFlow, AirFlow, S7 (rustfs), Grafana, Prometheus и Traefik.

Можно проверить наличие и содержание кластера следующими командами:
```
kind get clusters
kubectl config current-context
kubectl get nodes
kubectl get pods -A
```

kind get clusters должен вывести название вашего кластера. kubectl config current context должен вывести строку "kind-{название вашего кластера}". kubectl get nodes выведет ноду с control-plane, а kubectl get pods -A - список всех подов.

### 4.1 Важная команда для работы с кластером.
Для запуска python-кода, который использует сервисы вашего кластера, необходимо добавить их localhost-адреса в файл hosts. Для этого необходимо либо (в случае windows) зайти в powershell от имени администратора и ввести следующие команды:

```powershell
Add-Content -Path "$env:SystemRoot\System32\drivers\etc\hosts" -Value "`r`n127.0.0.1 mlflow.localhost airflow.localhost grafana.localhost bank.localhost s3.localhost s3-console.localhost"
ipconfig /flushdns
```

Либо (в случае bash) ввести следущие команды

```bash
echo "127.0.0.1 mlflow.localhost airflow.localhost grafana.localhost bank.localhost s3.localhost s3-console.localhost" | sudo tee -a /etc/hosts
sudo resolvectl flush-caches
```

## 5. Подготовка данных

Далее нужно загрузить в директорию свои данные и привязать их к dvc. Здесь на всякий случай приведу также код с привязыванием локального репозитория к удаленному репозиторию в github, так как он понадобится нам в дальнейшем для раскатки сервиса.

Команды для привязки удаленного репозитория:
```
git remote add origin https://github.com/NAME/REPO.git
git remote -v
```

Далее необходимо выполнить команды в dvc для ссоздания пользователей в хранилищах. Сами хранилища при этом создавать не нужно, так как они уже есть в .dvc/config.

```
uv run dvc remote modify --local laptop access_key_id dvcadmin
uv run dvc remote modify --local laptop secret_access_key dvc-secret-123
```

Теперь добавляем файл под управление в dvc и пушим его в хранилище. Первая команда нужна, если уже до этого отправили ваш файл с данными в git.

```
git rm -r --cached datasets/{your_dataset}.csv
uv run dvc add datasets/{your_dataset}.csv
uv run dvc push datasets/{your_dataset}.csv.dvc -r laptop
```

После этого рекомендуется сделать коммит в git, который сохранит в нем ваш датасет в .dvc файле в виде хэша.

## 6. Валидация данных и тренировку модели
Перед раскаткой сервиса необходимо разместить в mlflow натренированную на отвалидированных данных версию модели. Для этого необзодимо запустить файлы data.py и train.py. Здесь вам также понадобится 




