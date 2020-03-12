# DEMO: this file is irrelevant for the POC, I am not going to suggest any changes to how me build
# Docker images for our services
FROM python:3.7.6-slim
LABEL maintainer="Gengo <dev@gengo.com>"

ENV APPDIR /srv

RUN apt update && apt install -y gcc make
RUN pip3 install -U pip poetry==1.0.5
WORKDIR ${APPDIR}

COPY poetry.lock pyproject.toml ${APPDIR}/
RUN poetry config virtualenvs.create false && poetry install -n

ADD . ${APPDIR}/

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--reload", "authal.main:app"]
