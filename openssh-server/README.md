
# Setup

docker create --name=openssh-server  --hostname=aelz-server -e PUID=1000 -e PGID=1000   -e TZ=Europe/London -e USER_PASSWORD=password -e USER_NAME=ale -e SUDO_ACCESS=true -e PASSWORD_ACCESS=false -e PUBLIC_KEY="your key"  -p 2222:2222  --restart unless-stopped linuxserver/openssh-server

docker start openssh-server
