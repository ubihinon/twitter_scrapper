In order to launch the app.
1. build docker image: `sudo docker build -t twitter_scrapper . --no-cache`
2. run docker container: `sudo docker run -d --restart always -p 80:80 --name twitter_scrapper twitter_scrapper`

Data of user twitter can be got: http://localhost/users/{name}  
Example: http://localhost/users/Twitter, http://localhost/users/Twitter?limit=100  
Data by hashtag can be got: http://localhost:8000/hashtags/{hashtag name without '#'}    
Example: http://localhost/users/python, http://localhost/users/python?limit=100