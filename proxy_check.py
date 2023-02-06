import requests

# Load the list of proxy addresses from a file
with open("proxies.txt") as f:
    proxies = [line.strip() for line in f]

# Define the target URL to check the proxies against
target_url = "http://httpbin.org/get"

# Define the timeout for checking each proxy (in seconds)
timeout = 5

# Iterate through the list of proxies and check each one
for proxy in proxies:
    try:
        # Make a request to the target URL using the current proxy
        response = requests.get(target_url, proxies={"http": proxy}, timeout=timeout)
        # If the response is successful (status code 200), print a message indicating the working proxy
        if response.status_code == 200:
            print(f"Working proxy: {proxy}")
            break
    except requests.exceptions.RequestException as e:
        # If there's an exception during the request, move on to the next proxy
        continue
else:
    # If all proxies have been checked and none are working, print a message indicating that
    print("No working proxy found.")
