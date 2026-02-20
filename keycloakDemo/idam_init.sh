#!/bin/bash
#set -e
set -u


# Start keycloak in docker 
# https://www.keycloak.org/getting-started/getting-started-docker
# Connect when user and realm created:
# http://localhost:8080/auth/realms/<REALMNAME>/account/applications
# http://localhost:8080/auth/realms/testRealm/account/applications

curl="curl -v"

KEYCLOAK_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' recursing_williamson)
KEYCLOAK_ADDR=http://${KEYCLOAK_IP}:8080

MASREALM=master

# show keycloak authz config
# ${curl} "${KEYCLOAK_ADDR}/auth/realms/${REALM}/.well-known/openid-configuration" | jq .
# ${curl} "${KEYCLOAK_ADDR}/auth/realms/${REALM}/.well-known/uma2-configuration" | jq .

# admin user of keycloak
USERNAME=admin
PASSWORD=admin
CLIENT_ID=admin-cli

echo "AELZ init done"

# Example
# curl -v  -X POST localhost:8080/realms/master/protocol/openid-connect/token \
#  -d "client_id=admin-cli" -d "username=admin"  -d "password=admin" -d "grant_type=password"


# authenticate to admin-cli, get resource owner access token
resp=$(${curl} -X POST "${KEYCLOAK_ADDR}/realms/${MASREALM}/protocol/openid-connect/token" \
     -d 'grant_type=password' \
      -d "client_id=${CLIENT_ID}" \
       -d "username=${USERNAME}" \
        -d "password=${PASSWORD}" -d "scope=openid")
echo "${resp}" | jq -r .
ADMIN_TOKEN=$(echo "${resp}" | jq -r .access_token)
ADMIN_REFRESH_TOKEN=$(echo "${resp}" | jq -r .refresh_token)

#echo "AELZ admin token: ${ADMIN_TOKEN}"

# get admin user info
${curl} "${KEYCLOAK_ADDR}/realms/${MASREALM}/protocol/openid-connect/userinfo" \
     -H "Authorization: Bearer ${ADMIN_TOKEN}" \
         | jq .


# create user1 for demo, real user must be created in own realm but not in master
${curl} -X POST "${KEYCLOAK_ADDR}/admin/realms/${MASREALM}/users" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H 'Content-Type:application/json' \
    -d '{"username": "user1", "enabled": true, "credentials": [{"type": "password", "value": "password1", "temporary": false}]}' \
        | jq .

# create user2 for demo
${curl} -X POST "${KEYCLOAK_ADDR}/admin/realms/${MASREALM}/users" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H 'Content-Type:application/json' \
    -d '{"username": "user2", "enabled": true, "credentials": [{"type": "password", "value": "password2", "temporary": false}]}' \
        | jq .

# list users
${curl} "${KEYCLOAK_ADDR}/admin/realms/${MASREALM}/users" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" | jq .

# Next steps to create:
# - realm (tenant) for application specificv users
# - user roles and permissions
# - users
# - ....
