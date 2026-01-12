ARG PYTHON_VERSION=3.11
ARG GIT_REPO=https://github.com/beckzhang2012/DjangoBlog.git
ARG GIT_COMMIT=8648d394beca4def59d4a4e06ef41bb2d4279219

FROM python:${PYTHON_VERSION}-slim AS code-fetcher

# 安装 git 以便锁定仓库版本
RUN apt-get update && \
    apt-get install --no-install-recommends -y git && \
    rm -rf /var/lib/apt/lists/*

ARG GIT_REPO
ARG GIT_COMMIT

WORKDIR /app

RUN echo "========================================" && \
    echo "Cloning repository: ${GIT_REPO}" && \
    echo "Checking out: ${GIT_COMMIT}" && \
    echo "========================================" && \
    git clone ${GIT_REPO} . && \
    git checkout ${GIT_COMMIT} && \
    rm -rf .git

FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code/djangoblog

# 系统依赖：MySQL client 开发库、gettext
RUN apt-get update && \
    apt-get install --no-install-recommends -y default-libmysqlclient-dev gettext && \
    rm -rf /var/lib/apt/lists/*

COPY --from=code-fetcher /app .

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn[gevent] && \
    pip cache purge

RUN chmod +x deploy/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["deploy/entrypoint.sh"]
