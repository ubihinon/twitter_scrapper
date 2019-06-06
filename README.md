In order to launch the app.
1. Install Docker on your local machine
2. build docker image: `sudo docker build -t twitter_scrapper . --no-cache`
3. run docker container: `sudo docker run -d --restart always -p 80:80 --name twitter_scrapper twitter_scrapper`

Swagger documentation: http://localhost:80/docs
Data of user twitter can be got: http://localhost:80/users/{name}  
Example: http://localhost:80/users/Twitter, http://localhost:80/users/Twitter?limit=100  
Data by hashtag can be got: http://localhost/hashtags/{hashtag name without '#'}    
Example: http://localhost:80/users/python, http://localhost:80/users/python?limit=100

If you want to launch tests you need to create `dev.py` file in `/twitter_scrapper/settings` 
and copy content from `dev.py.template`. After that you can launch tests.