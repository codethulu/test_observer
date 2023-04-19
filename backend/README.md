# Test Observer Backend

## Development Setup

This project supports [microk8s](https://microk8s.io/) development environment with the help of [Skaffold](https://skaffold.dev/). It also uses [Poetry](https://python-poetry.org/) for dependency management.

### 1. Install required tools

- Install [docker](https://snapcraft.io/docker) and setup permissions
- Install [microk8s](https://microk8s.io/docs/getting-started) and setup permissions
- Install [Skaffold](https://skaffold.dev/docs/install/#standalone-binary)
- Install [Poetry](https://python-poetry.org/docs/#installation)

### 2. Setup Skaffold and microk8s

- Skaffold requires a k8s registry to push and pull images from so just run `$ microk8s enable registry`
- Allow pods to communicate together in microk8s through CoreDNS by running `$ microk8s enable dns` 
- Allow persistent volume claims to claim storage using `$ microk8s enable hostpath-storage`
- Skaffold uses kubectl so create an alias for `microk8s.kubectl` using `snap alias microk8s.kubectl kubectl`
- In order for Skaffold to connect to microk8s it needs it's configuration, so run `$ microk8s config > ~/.kube/config`. Note that if you get an error connecting to the cluster, it could be that the cluster's IP has changed for some reason, so you have to run this command again

### 3. Install python dependencies for linting and completions

While technically not required to run the code, it helps to have dependencies installed on host system to get code completions and linting. To do that just run `$ poetry install`. Note that poetry will create a virtual environment for you, but if you want poetry to create that virtual environment inside this project's directory just run `$ poetry config virtualenvs.in-project true` before installing dependencies.

### 4. Start the development environment

Assuming that your microk8s cluster is running, you can start the development environment by simply running `$ skaffold dev`. This command will build the docker images and push them to your microk8s registry, then apply your k8s manifest to start the cluster and pull those images. Additionally, skaffold will watch for file changes and either sync them directly inside the running containers or rebuild and redeploy k8s cluster for you automatically.

## Dependency Management

### Add/Install dependency

`$ poetry add foo`

If it's a dev dependency

`$ poetry add --group dev foo`

### Remove/Uninstall dependency

`$ poetry remove foo`

## Database Migrations

The project uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) to manage database migrations. Migrations will be applied automatically when running Skaffold. But making changes to data models requires manually creating and applying migrations.

### Create Migrations

For more information on how to create migrations, please check [Alembic docs](https://alembic.sqlalchemy.org/en/latest/). Note, that it's worth noting that Alembic can help [auto generate migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html) based on differences between SQLAlchemy ORMs and the actual database. But developers have to check these migrations to make sure they're fine.

### Applying Migrations

Since the database is in microk8s cluster, migrations have to be applied inside the cluster and not on the host machine. To do that we can just run the migrations on our api service which will run in one of the api pods through:

`$ kubectl exec -it service/test-observer-api -- alembic upgrade head`