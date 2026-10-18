# Quickstart
Ниже приведем последовательность команд, которые нужно проделать для запуска кластера и сервисов у себя на локальном компьютере.

## Клонирование репозитория и настройка окружения
git clone https://github.com/Fetis789/BankMarketingPetModel.git .

## Установка и настройка uv
### Установка
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
```

### Настройка
```
uv --version
uv python install 3.11
uv sync --locked
uv run python --version
```

## Установка и проверка docker, kind, kubectl, helm, curl
Установка всех сервисов
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




Проверка всех сервисов
```
docker version
docker info
kind version
kubectl version --client
helm version
curl --version
```

##
