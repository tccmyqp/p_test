from flask import Flask, jsonify, request
import requests
import logging
import datetime
import sys
# import unittest

# ------------------------------------------------------ прокси
proxy = {
    "http": "http://174.70.1.210:8080",
    # "https": "https://<proxy_host>:<proxy_port>"
}

owner = "tccmyqp"
repo = "p_test"
                      
github_link = "https://api.github.com/repos"
local_link = "http://127.0.0.1:5000/repo"

def compile_index_page(local_link,owner,repo, proxy):
    change_data_form = """
                    <form action="http://localhost:5000/form" method="post">
                        <label for="owner_field">owner:</label>
                        <input type="text" name="owner_field" id="owner_field">
                        <label for="repo_field">repo:  </label>
                        <input type="text" name="repo_field" id="repo_field">
                        <input type="submit" value="Изменить">
                    </form>
                    """
    
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

    {change_data_form}<p>

    <a href={details_link}>{details_link}</a><p>
    <a href={pulls_link}>{pulls_link}</a><p>
    <a href={stale_link}>{stale_link}</a><p>
    <a href={issues_link}>{issues_link}</a><p>
    <a href={forks_link}>{forks_link}</a><p>

    </body>
    </html>
    """
    return index_page

index_page = compile_index_page(local_link, owner, repo, proxy)


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
logger.info("-------------- app run -----------------")


#------------------------------------------------------- Flask
app = Flask(__name__)


#------------------------------------------------------- отображает индексную станицу
@app.route("/")
def index():  
    return index_page


#------------------------------------------------------- получает данные и отображает измененную индексную станицу
@app.route('/form', methods=['POST'])
def receive_data():
    global owner, repo, index_page
    owner = request.form['owner_field']
    repo = request.form['repo_field']
    index_page = compile_index_page(local_link, owner, repo, proxy)   
    return index_page


def request_processing(link):
    try:
        response = requests.get(link, proxies=proxy)
        if response.status_code == 200:
            logger.info(f"request {link}")
            return response
        else:
            logger.warning(f'Failed to get {link}. Response status code: {response.status_code}')
            return response
    except:
        e = sys.exc_info()[1]
        logger.exception(f'Failed to get {link}. Response status code: {response.status_code}. Exeption: {e.args[0]}')
        return response

#-------------------------------------------------------/ отображает repo details
@app.route('/repo/<owner>/<repo>/details', methods=['GET'])
def repo_details(owner: str, repo: str):
    link = f'{github_link}/{owner}/{repo}'
    return jsonify(request_processing(link).json())

    
#-------------------------------------------------------/ отображает repo pulls
@app.route('/repo/<owner>/<repo>/pulls', methods=['GET'])
def repo_pulls(owner: str, repo: str)/:
    link = f'{github_link}/{owner}/{repo}/pulls'
    return jsonify(request_processing(link).json())
    
    
#-------------------------------------------------------/ отображает pulls stale
@app.route('/repo/<owner>/<repo>/pulls/stale', methods=['GET'])
def repo_stale_pulls(owner: str, repo: str):
    pulls = requests.get(f'https://api.github.com/repos/{owner}/{repo}/pulls', proxies=proxy).json()
    stale_pulls = [pull for pull in pulls if (datetime.now() - datetime.strptime(pull['updated_at'], '%Y-%m-%dT%H:%M:%SZ')).days >= 14]
    return jsonify(stale_pulls)
    
    
#-------------------------------------------------------/ отображает repo issues
@app.route('/repo/<owner>/<repo>/issues', methods=['GET'])
def repo_issues(owner: str, repo: str):
    link = f'{github_link}/{owner}/{repo}/issues'
    return jsonify(request_processing(link).json())


#-------------------------------------------------------/ отображает repo forks
@app.route('/repo/<owner>/<repo>/forks', methods=['GET'])
def repo_forks(owner: str, repo: str):
    link = f'{github_link}/{owner}/{repo}/forks'
    return jsonify(request_processing(link).json())
    
    
if __name__ == '__main__':
    app.run(debug=True)
