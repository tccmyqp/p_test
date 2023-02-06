from flask import Flask, jsonify, request
import requests
import logging
import datetime
# import unittest

# ------------------------------------------------------ прокси
proxy = {
    "http": "http://174.70.1.210:8080",
    # "https": "https://<proxy_host>:<proxy_port>"
}

form = """
<form action="http://localhost:5000/form" method="post">
    <label for="owner_field">owner:</label>
    <input type="text" name="owner_field" id="owner_field">
    <label for="repo_field">repo:  </label>
    <input type="text" name="repo_field" id="repo_field">
    <input type="submit" value="Изменить">
</form>
"""

owner = "tccmyqp"
repo = "p_test"

github_link = "https://api.github.com/repos"
local_link = "http://127.0.0.1:5000/repo"

details_link = f'{local_link}/{owner}/{repo}/details'
pulls_link = f'{local_link}/{owner}/{repo}/pulls'
stale_link = f'{local_link}/{owner}/{repo}/pulls/stale'
issues_link = f'{local_link}/{owner}/{repo}/issues'
forks_link = f'{local_link}/{owner}/{repo}/forks'

index_page = f"""
<html>
<body>
Hello, welcome to the Github REST API proxy!<p>

using proxy: {proxy["http"]}<p>

owner = {owner}, repo = {repo}<p>

{form}<p>

<a href={details_link}>{details_link}</a><p>
<a href={pulls_link}>{pulls_link}</a><p>
<a href={stale_link}>{stale_link}</a><p>
<a href={issues_link}>{issues_link}</a><p>
<a href={forks_link}>{forks_link}</a><p>

</body>
</html>
"""


#------------------------------------------------------ логгер
# Define the logger and set its logging level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define a handler to write the log messages to a file
file_handler = logging.FileHandler("api.log")
file_handler.setLevel(logging.INFO)

# Define the format of the log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

#------------------------------------------------------ Flask
logger.info("-------------- app run -----------------")

app = Flask(__name__)

@app.route("/")
def index():  
    return index_page

@app.route('/form', methods=['POST'])
def receive_data():
    global owner, repo, index_page
    owner = request.form['owner_field']
    repo = request.form['repo_field']
    
    details_link = f'{local_link}/{owner}/{repo}/details'
    pulls_link = f'{local_link}/{owner}/{repo}/pulls'
    stale_link = f'{local_link}/{owner}/{repo}/pulls/stale'
    issues_link = f'{local_link}/{owner}/{repo}/issues'
    forks_link = f'{local_link}/{owner}/{repo}/forks'
    
    index_page = f"""
                <html>
                <body>
                Hello, welcome to the Github REST API proxy!<p>

                using proxy: {proxy["http"]}<p>

                owner = {owner}, repo = {repo}<p>

                {form}<p>

                <a href={details_link}>{details_link}</a><p>
                <a href={pulls_link}>{pulls_link}</a><p>
                <a href={stale_link}>{stale_link}</a><p>
                <a href={issues_link}>{issues_link}</a><p>
                <a href={forks_link}>{forks_link}</a><p>

                </body>
                </html>
                """
    
    # return "Data received: textfield1 = " + text1 + ", textfield2 = " + text2
    return index_page

@app.route('/repo/<owner>/<repo>/details', methods=['GET'])
def repo_details(owner: str, repo: str):
    try:
        response = requests.get(f'{github_link}/{owner}/{repo}', proxies=proxy)
        if response.status_code == 200:
            logger.info(f"request repo details from the Github API {owner}/{repo}")
            return jsonify(response.json())
    except:
        logger.error(f'Failed to get repo details from the Github API {owner}/{repo}. Response status code: {response.status_code}')
    
    
@app.route('/repo/<owner>/<repo>/pulls', methods=['GET'])
def repo_pulls(owner: str, repo: str):
    try:
        response = requests.get(f'{github_link}/{owner}/{repo}/pulls', proxies=proxy)
        if response.status_code == 200:
            logger.info(f"request pulls from the Github API {owner}/{repo}")
            return jsonify(response.json())
    except:
        logger.error(f'Failed to get repo pulls from the Github API {owner}/{repo}. Response status code: {response.status_code}')
            
    
@app.route('/repo/<owner>/<repo>/pulls/stale', methods=['GET'])
def repo_stale_pulls(owner: str, repo: str):
    try:
        response = requests.get(f'{github_link}/{owner}/{repo}/pulls', proxies=proxy)
        
        if response.status_code == 200:
            pulls = response.json()
        
            logger.info(f"request pulls stale from the Github API {owner}/{repo}")
            stale_pulls = [pull for pull in pulls if (datetime.now() - datetime.strptime(pull['updated_at'], '%Y-%m-%dT%H:%M:%SZ')).days >= 14]
            return jsonify(stale_pulls)
    except:
        logger.error(f'Failed to get repo pulls stale from the Github API {owner}/{repo}. Response status code: {response.status_code}')


@app.route('/repo/<owner>/<repo>/issues', methods=['GET'])
def repo_issues(owner: str, repo: str):
    try:
        response = requests.get(f'{github_link}/{owner}/{repo}/issues', proxies=proxy)
        if response.status_code == 200:
            logger.info(f"request repo issues from the Github API {owner}/{repo}")
            return jsonify(response.json())
    except:
        logger.error(f'Failed to get repo issues stale from the Github API {owner}/{repo}. Response status code: {response.status_code}')


@app.route('/repo/<owner>/<repo>/forks', methods=['GET'])
def repo_forks(owner: str, repo: str):
    try:
        response = requests.get(f'{github_link}/{owner}/{repo}/forks', proxies=proxy)
        if response.status_code == 200:
            logger.info(f"request repo forks from the Github API {owner}/{repo}")
            return jsonify(response.json())
    except:
        logger.error(f'Failed to get repo forks stale from the Github API {owner}/{repo}. Response status code: {response.status_code}')

if __name__ == '__main__':
    app.run(debug=True)
