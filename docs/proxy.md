# Working with Proxies and Dependency Installs

When running tests locally, dependency installation may be blocked by corporate or sandbox network rules. These steps help `pip` and Docker-based workflows succeed behind an HTTP/HTTPS proxy.

## Configure proxy environment

Set the standard proxy environment variables before running `pip install` or any `make` target (e.g., `make dev` or `make test-unit`). Include credentials if required, and ensure both lowercase and uppercase variants are present for compatibility.

```bash
export http_proxy="http://USERNAME:PASSWORD@proxy.example.com:8080"
export https_proxy="http://USERNAME:PASSWORD@proxy.example.com:8080"
export HTTP_PROXY="$http_proxy"
export HTTPS_PROXY="$https_proxy"
```

If your proxy uses a custom CA certificate, point `REQUESTS_CA_BUNDLE` (used by `pip`) to your certificate chain:

```bash
export REQUESTS_CA_BUNDLE="/path/to/corp-ca.crt"
```

## Persist proxy for pip

You can set a persistent pip configuration so every install uses the proxy automatically.

```bash
pip config set global.proxy "$http_proxy"
# optionally set your internal mirror as the primary index
pip config set global.index-url "https://<internal-mirror-host>/simple"
```

To avoid storing credentials in plain text, rely on environment variables instead of the config file when possible.

## Using a local or mirrored index

If internet access is blocked, use an internal PyPI mirror or wheelhouse. Point pip at the mirror and disable the public index fallback:

```bash
pip install --no-cache-dir --no-index \
  --find-links https://<internal-mirror-host>/simple \
  -r requirements-dev.txt
```

For fully offline installs, download wheels on a machine with access and copy them into a `./wheelhouse` directory:

```bash
pip download -r requirements-dev.txt -d wheelhouse
pip install --no-index --find-links wheelhouse -r requirements-dev.txt
```

## Docker and docker-compose

When running services via `docker-compose`, pass the proxy variables through so build and run steps can fetch dependencies:

```bash
HTTP_PROXY=$http_proxy HTTPS_PROXY=$https_proxy \
  docker-compose --env-file infra/.env.example up --build
```

If your proxy intercepts TLS, add your CA certificate to Docker’s trust store (typically `/etc/docker/certs.d/<registry>/ca.crt`) and restart the daemon.

## Verifying installs before tests

After configuring the proxy, validate dependency installation before running the test targets:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
make test-unit
```

If installation still fails, check for authentication prompts or SSL errors and re-validate the proxy variables and CA bundle paths.
