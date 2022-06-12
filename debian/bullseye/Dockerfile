ARG VARIANT=bullseye
FROM debian:$VARIANT
ENV VARIANT=${VARIANT:-bullseye}

ARG DEBIAN_FRONTEND="noninteractive"

RUN set -eux; apt-get update; \
    apt-get --assume-yes install --no-install-recommends \
    apt-utils \
    ; \
    apt-get --assume-yes autoremove; \
    apt-get --assume-yes clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*;


# Update installed packages
RUN set -eux; apt-get update; \
    apt-get --assume-yes upgrade --no-install-recommends; \
    apt-get --assume-yes autoremove; \
    apt-get --assume-yes clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*;


# Install some additional helpful packages
RUN set -eux; apt-get update; \
    apt-get --assume-yes install --no-install-recommends \
    iproute2 \
    iputils-ping \
    iputils-tracepath \
    less \
    nano-tiny \
    tree \
    ; \
    apt-get --assume-yes autoremove; \
    apt-get --assume-yes clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*; 

RUN set -eux; \
    if [ "$VARIANT" == "bullseye" ]; then \
    apt-get --assume-yes install --no-install-recommends \
    man-db \
    manpages \
    ; \
    apt-get --assume-yes autoremove; \
    apt-get --assume-yes clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*; \
    fi
