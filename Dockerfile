FROM python:3.12-alpine

# Системные зависимости: Chromium + chromedriver + Java для Allure
RUN apk add --no-cache \
    ca-certificates \
    chromium \
    chromium-chromedriver \
    tzdata \
    openjdk17-jre \
    curl \
    tar \
    wget \
    && update-ca-certificates

# Allure CLI - 2.16.2 не существует для allure-commandline в Maven (есть 2.16.0/2.16.1->2.17.0), используем актуальную 2.32.0
ENV ALLURE_VERSION=2.32.0
RUN set -eux; \
    curl -fsSL --retry 3 --retry-delay 5 -o /tmp/allure.tgz "https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/${ALLURE_VERSION}/allure-commandline-${ALLURE_VERSION}.tgz" || \
    wget -qO /tmp/allure.tgz "https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/${ALLURE_VERSION}/allure-commandline-${ALLURE_VERSION}.tgz"; \
    ls -lh /tmp/allure.tgz; \
    tar -zxvf /tmp/allure.tgz -C /opt/; \
    ln -sf /opt/allure-${ALLURE_VERSION}/bin/allure /usr/bin/allure; \
    rm /tmp/allure.tgz; \
    allure --version

WORKDIR /usr/workspace

COPY ./requirements.txt /usr/workspace
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /usr/workspace

CMD ["python", "-m", "pytest", "--alluredir=allure-results"]