# https://github.com/nektos/act/issues/418#issuecomment-727261137
FROM ubuntu:20.04

RUN apt-get update \
  && apt-get upgrade -y \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  build-essential \
  curl \
  git \
  zip \
  unzip \
  nodejs \
  npm \
  && rm -rf /var/lib/apt/lists/*