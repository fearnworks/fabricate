FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MPLCONFIGDIR /tmp/matplotlib

# Install dependencies
RUN --mount=type=cache,target=/var/cache/apt,id=apt \
    apt-get update && \
    apt-get install --no-install-recommends -y git vim build-essential python3.11-dev python3-pip procps net-tools tini && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3.11 -m pip install --upgrade pip

# Create app directory and change ownership to appuser
RUN mkdir /app 
COPY ./backend/requirements/requirements.in /app/requirements.txt
RUN --mount=type=cache,target=~/.cache/pip \
    python3.11 -m pip install -r /app/requirements.txt


#Set working directory to /app
WORKDIR /app

COPY ./backend /app/backend
RUN pip install -e /app/backend
RUN chmod +x /app/backend/scripts/run.sh
WORKDIR /app/backend
RUN python3.11 -m pip install /app/backend
EXPOSE 28100
ENTRYPOINT ["tini", "--", "/app/backend/scripts/run.sh"]
# CMD ["tail", "-f", "/dev/null"]