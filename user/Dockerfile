FROM alemna/debian:bullseye

#ARG DEBIAN_FRONTEND=noninteractive

# Install some additional helpful packages
RUN set -eux; apt-get update; \
    apt-get --assume-yes install --no-install-recommends \
    # AppArmor
    apparmor apparmor-utils apparmor-profiles-extra auditd \
    # dnsutils: Mainly, provides the 'dig' command for DNS lookups. Also
    # provides the (older) 'nslookup' command. 
    bind9-dnsutils \
    # CA Certificates: A base set of certificates from common certificate 
    # authorities.
    #   (highly recommended for both git and wget)
    ca-certificates \
    # cURL
    curl \
    # OpenDoas: A small sudo replacement
    doas \
    # Fish: The Friendly Interactive Shell
    fish \
    # Git: Version control software
    git \
    # GnuPG: A tool to encrypt data and create digital signatures.
    #gnupg \
    # htop
    htop \
    # less: A terminal pager program
    less \
    # lft: A really, really sweet traceroute utility. Also provides the
    # 'whob' command.
    lft \
    # lsof: A utility to view all open files
    lsof \
    # man: Manual pages for Unix
    man-db manpages \
    # moreutils: A handful of simple apps (like 'ifdata', 'ts', and 'chronic')
    # that didn't make it into the original Unix coreutils.
    moreutils \
    # peco: An interactive text filterer
    peco \
    # tldr
    #   --> also requires git
    tldr \
    # tmux
    tmux \
    # UFW: An uncomplicated firewall
    ufw \
    # Unbound: local DNS
    #   --> openresolv: a tool for autoconfiguring the system to use unbound
    unbound openresolv \
    # wget: A tool to download files
    wget \
    ; \
    #mkdir --parents ~/.local/share/tldr; \
    #tldr --update; \
    apt-get --assume-yes autoremove; \
    apt-get --assume-yes clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*;

# See also:
# https://ostechnix.com/some-useful-tools-for-linux-system-admins/
# http://cdn.ttgtmedia.com/rms/pdf/linux_commands_eguide.pdf
# https://www.linuxlinks.com/outstanding-linux-utilities-maximize-productivity/
# GOOD -> https://www.linuxlinks.com/best-free-open-source-software/
# https://ostechnix.com/how-to-create-and-maintain-your-own-man-pages/
# https://ostechnix.com/kmdr-display-cli-commands-explanation-in-terminal/
# https://ostechnix.com/how-to-create-and-maintain-your-own-man-pages/
# https://www.linuxlinks.com/excellent-utilities-watson-cli-tool-track-time/2/
# https://www.explainshell.com/

## Maybe also
# neofetch (DEFINITELY --no-install-recommends)
# nmap
# snort
# nc (netcat)
# netstat
# tcpstat
# tcpdump
# ethtool (not super useful in containers)
# ifupdown (add to base?)
# parted
# fdisk
# tldr (community documentation)
# nload (simple network monitor)
# firejail
# fail2ban
# openssh-server openssh-client
# rsyslog
# # WireGuard: A simple VPN.
#  ---> The 'wireguard-dkms' modules is so we don't need to download a new kernal image
#wireguard wireguard-tools wireguard-dkms\
