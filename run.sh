# docker rm -f pic_server
# docker rmi pic:latest

# docker build -t pic:latest .
# docker run -itd -p 8001:8001 --name pic_server pic:latest

docker-compose down
docker-compose rm
docker-compose build
docker-compose up