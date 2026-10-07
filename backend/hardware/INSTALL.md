# install dependancies:
sudo apt install python3 python3-serial

# copy files to target
# I've put them in my homedir

# tweak config.py

# create systemd service:
sudo vim /lib/systemd/system/laadpaal.service
##
[Unit]
Description=Laadpaal
After=network-online.target

[Service]
ExecStart=/home/maarten/main.py
WorkingDirectory=/home/maarten/
Restart=always

[Install]
WantedBy=multi-user.target
## EOF

# enable systemd service
sudo systemctl enable laadpaal
sudo systemctl start laadpaal
sudo systemctl status laadpaal
