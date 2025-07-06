FROM python:3.12-slim

ARG USERNAME=immich-tiktok-remover
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the immich-tiktok-remover user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER $USERNAME

WORKDIR /home/immich-tiktok-remover

RUN mkdir /home/immich-tiktok-remover/.local

ENV PIP_NO_CACHE_DIR=off 

COPY src/ .
COPY requirements.txt .
COPY run_docker.sh .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["./run_docker.sh"]

