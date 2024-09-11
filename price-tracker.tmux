# Create a new session named "price-tracker"
new -s price-tracker -n backend
send-keys "conda activate price-tracker && cd /home/k/projects/price-tracker/backend/app && uvicorn main:app --reload" C-m

# Split the window vertically and start PostgreSQL in the new pane
split-window -h
send-keys "sudo -i -u postgres" C-m
send-keys "aa1234" C-m
send-keys "psql" C-m
send-keys "\\c testdb1" C-m

# Split the window horizontally and activate Conda in the new pane
split-window -v
send-keys "conda activate price-tracker && cd /home/k/projects/price-tracker/backend" C-m

# Create a new window and start npm in the frontend window
new-window -n frontend
send-keys "conda activate price-tracker && cd /home/k/projects/price-tracker/frontend && npm start" C-m

# Select the first window (backend window) to be active by default
select-window -t 0
