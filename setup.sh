# Network name
NETWORK_NAME="fabricate-network"

# Check if the network exists
if [ -z "$(docker network ls --filter name=^${NETWORK_NAME}$ --format '{{.Name}}')" ]; then
    echo "Network ${NETWORK_NAME} does not exist. Creating it..."
    docker network create ${NETWORK_NAME}
else
    echo "Network ${NETWORK_NAME} already exists."
fi

# Run Docker Compose
docker compose up --build