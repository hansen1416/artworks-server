from src.app import app

if __name__ == "__main__":

    """
    [program:artworks]
    command = /root/artworks-server/venv/bin/python3 /root/artworks-server/venv/bin/gunicorn --chdir /root/artworks-server/ --config /root/artworks-server/gunicorn.conf app:app
    user = root  # Replace with your username
    autostart = false
    autorestart = true
    """

    app.run(host="0.0.0.0", port=6301, debug=True)
