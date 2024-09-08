import requests
from bs4 import BeautifulSoup
import time

def make_request(url, method='GET', headers=None, data=None, auth=None):
    try:
        # Make the HTTP request
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, auth=auth)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, data=data, auth=auth)
        else:
            print(f"Unsupported HTTP method: {method}")
            return

        # Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Response Body (First 500 chars):\n{response.text[:500]}")

        # Parse and analyze HTML (optional)
        if 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"Title: {soup.title.string if soup.title else 'No title found'}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    url = input("Enter the URL to test (e.g., http://localhost:8000): ")
    method = input("Enter HTTP method (GET or POST): ").strip().upper()

    if method == 'POST':
        data = input("Enter POST data (key=value pairs separated by &): ")
        data = dict(item.split('=') for item in data.split('&'))
    else:
        data = None

    headers = {
        'User-Agent': 'Python HTTP Client',
        'Accept': 'text/html,application/xhtml+xml'
    }

    auth = None
    if input("Do you need basic authentication? (yes/no): ").strip().lower() == 'yes':
        username = input("Enter username: ")
        password = input("Enter password: ")
        auth = (username, password)

    if method == 'GET':
        num_requests = int(input("Enter the number of GET requests to make: "))
        delay = float(input("Enter the delay between requests (in seconds, 0 for no delay): "))

        for _ in range(num_requests):
            make_request(url, method=method, headers=headers, data=data, auth=auth)
            time.sleep(delay)
    else:
        make_request(url, method=method, headers=headers, data=data, auth=auth)

if __name__ == "__main__":
   main()