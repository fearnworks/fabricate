FROM node:lts

RUN --mount=type=cache,target=/var/cache/apt,id=apt \
    apt-get update && \
    apt-get install --no-install-recommends -y git vim procps net-tools tini && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
# install simple http server for serving static content
RUN npm install -g http-server

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY ./webui/package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY ./webui /app/webui
RUN chmod +x /app/webui/run_webui.sh
# build app for production with minification
# RUN npm run dev

EXPOSE 8080
ENTRYPOINT ["tini", "--", "/app/webui/run_webui.sh"]
# CMD ["tail", "-f", "/dev/null"]