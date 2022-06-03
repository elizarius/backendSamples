#!/bin/bash
#set -e
set -u

curl="curl -v"

KEYCLOAK_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' keycloak_cont_name)
KEYCLOAK_ADDR=http://${KEYCLOAK_IP}:8080

REALM=master

# show keycloak authz config
#${curl} "${KEYCLOAK_ADDR}/auth/realms/${REALM}/.well-known/openid-configuration" | jq .
#${curl} "${KEYCLOAK_ADDR}/auth/realms/${REALM}/.well-known/uma2-configuration" | jq .

# admin user of keycloak
USERNAME=kcadminid
PASSWORD=kcpasswd
CLIENT_ID=admin-cli

echo "AELZ init done"


p=$(${curl} -X POST "${KEYCLOAK_ADDR}/auth/realms/${REALM}/protocol/openid-connect/token" \
     -d 'grant_type=password' \
      -d "client_id=${CLIENT_ID}" \
       -d "username=${USERNAME}" \
        -d "password=${PASSWORD}")
echo "${resp}" | jq -r .
# authenticate to admin-cli
# get resource owner access token
resp=$(${curl} -X POST "${KEYCLOAK_ADDR}/auth/realms/${REALM}/protocol/openid-connect/token" \
     -d 'grant_type=password' \
      -d "client_id=${CLIENT_ID}" \
       -d "username=${USERNAME}" \
        -d "password=${PASSWORD}")
echo "${resp}" | jq -r .
ADMIN_TOKEN=$(echo "${resp}" | jq -r .access_token)
ADMIN_REFRESH_TOKEN=$(echo "${resp}" | jq -r .refresh_token)



# get admin user info
${curl} "${KEYCLOAK_ADDR}/auth/realms/${REALM}/protocol/openid-connect/userinfo" \
     -H "Authorization: Bearer ${ADMIN_TOKEN}" \
         | jq .

# create user1
${curl} -X POST "${KEYCLOAK_ADDR}/auth/admin/realms/${REALM}/users" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H 'Content-Type:application/json' \
    -d '{"username": "user1", "enabled": true, "credentials": [{"type": "password", "value": "password1", "temporary": false}]}' \
        | jq .
 
# create user2
${curl} -X POST "${KEYCLOAK_ADDR}/auth/admin/realms/${REALM}/users" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H 'Content-Type:application/json' \
    -d '{"username": "user2", "enabled": true, "credentials": [{"type": "password", "value": "password1", "temporary": false}]}' \
        | jq .
 
# list users
${curl} "${KEYCLOAK_ADDR}/auth/admin/realms/${REALM}/users" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" | jq .
 
# first create client "myapp" via UI
CLIENT_ID=myapp
CLIENT_SECRET=4df3f06c-711f-4269-b6b3-39584a2067de
USERNAME=user2
PASSWORD=password1
 
# get token for client access
# get resource owner access token
# access token encodes roles
resp=$(${curl} -X POST "${KEYCLOAK_ADDR}/auth/realms/${REALM}/protocol/openid-connect/token" \
     -d 'grant_type=password' \
      -d "client_id=${CLIENT_ID}" \
       -d "client_secret=${CLIENT_SECRET}" \
        -d "username=${USERNAME}" \
         -d "password=${PASSWORD}")
echo "${resp}" | jq -r .
ACCESS_TOKEN=$(echo "${resp}" | jq -r .access_token)
 
${curl} "${KEYCLOAK_ADDR}/auth/realms/${REALM}/protocol/openid-connect/userinfo" \
     -H "Authorization: Bearer ${ACCESS_TOKEN}" \
         | jq .


