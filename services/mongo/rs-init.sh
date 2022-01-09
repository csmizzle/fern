#!/bin/bash

echo "Starting replica set initialize"
until mongosh --host mongodb1 --eval "print(\"waited for connection\")"
do
    sleep 2
done
echo "Connection finished"
echo "Creating replica set"
mongosh --host mongodb1 <<EOF
rs.initiate(
  {
    _id : 'rs0',
    members: [
      { _id : 0, host : "mongo:27017" },
      { _id : 1, host : "mongodb2:27017" }
    ]
  }
)
EOF
echo "replica set created"