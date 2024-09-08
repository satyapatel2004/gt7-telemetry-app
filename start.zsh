#!/bin/zsh

# Open the first terminal instance for npm start (React app)
osascript <<EOF
tell application "Terminal"
    do script "cd Desktop/gt7/frontend && npm start"
end tell
EOF

# Add a delay to ensure the React app starts first
sleep 1

# Open the second terminal instance for the Flask server
osascript <<EOF
tell application "Terminal"
    do script "cd Desktop/gt7 && source venv/bin/activate && cd server && gunicorn -k gevent -w 1 -b 127.0.0.1:5000 app:app"
end tell
EOF

# Add a delay to ensure the Flask server starts before the client script
sleep 1

# Open the third terminal instance for the client script
osascript <<EOF
tell application "Terminal"
    do script "cd Desktop/gt7 && source venv/bin/activate && cd client_scripts && python3.11 main.py"
end tell
EOF 