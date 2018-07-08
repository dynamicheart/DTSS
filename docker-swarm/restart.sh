docker stack rm zk
docker stack rm kafka
docker stack rm server
docker stack rm mongo
docker stack rm express
docker stack rm rater
docker stack deploy -c zk.yml zk
docker stack deploy -c kafka.yml kafka
docker stack deploy -c server.yml server
docker stack deploy -c mongo-cluster.yml mongo
docker stack deploy -c express.yml express
docker stack deploy -c yjb/exchange_rater/rater.yml rater
