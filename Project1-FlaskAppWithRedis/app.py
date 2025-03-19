from flask import Flask, render_template_string
import redis
import os
import socket

app = Flask(__name__)
# Connection to Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
environment = os.environ.get('ENVIRONMENT', 'development')  # Getting info about ENV
cache = redis.Redis(host=redis_host, port=6379, socket_connect_timeout=2, socket_timeout=2)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    # Use different keys depending on ENV
    counter_key = f"hits_{environment}"
    
    try:
        visits = cache.incr(counter_key)
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
        visits = "Redis unavailable"
    
    # Specify name of ENV to display
    env_display_name = "PRODUCTION" if environment == "production" else "DEVELOPMENT"
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kubernetes Demo - {{ env_display_name }}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
            .container { max-width: 800px; margin: 0 auto; }
            .info { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
            .count { font-size: 24px; font-weight: bold; color: #3366cc; }
            .env-prod { background-color: #ffdddd; }
            .env-dev { background-color: #ddffdd; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Kubernetes DEMO App - {{ env_display_name }}</h1>
            <div class="info {% if environment == 'production' %}env-prod{% else %}env-dev{% endif %}">
                <p>Pod name: <strong>{{ hostname }}</strong></p>
                <p>Environment: <strong>{{ env_display_name }}</strong></p>
                <p>Number of visits to this environment: <span class="count">{{ visits }}</span></p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, hostname=hostname, visits=visits, environment=environment, env_display_name=env_display_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)