import ipaddress
import os

from flask import Flask, request

app = Flask(__name__)


def get_user_ip():
    """Returns the user's IP address from the request."""
    if not request:
        return None

    # Checks for 'X-Forwarded-For' header when using a proxy or load balancer
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # In cases of multiple IPs, the left-most one is the real client IP address
        ip = forwarded_for.split(',')[0].strip()
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            ip = request.remote_addr
    else:
        # Fallback to request's remote address
        ip = request.remote_addr
    return ip


@app.route('/')
def index():
    user_ip = get_user_ip()
    return f'Your IP address is: {user_ip}'


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug)
