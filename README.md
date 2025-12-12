******SETUP NGINX******
- Go to https://nginx.org/en/download.html and select appropriate mainline version (macOS might need installation via Homebrew?)
- I (Windows 10) chose nginx/Windows-1.29.4 (mainline)
- In C:\nginx\conf\nginx.conf change the port in the 'listen' directive --> from 80 to 8123
	--> example 
	server {
    		listen       80; //change this to 8123
    		server_name  localhost;
   		...
	}



- ***Start NGINX server (Powershell)***:
	start nginx

- ***Stop NGINX server (Powershell)***:
	.\nginx -s stop (Why .\?? Idk my patience just died)

- ***Reload NGINX server (Powershell)***:
	.\nginx -s reload (must be running beforehand; used for config changes)



******WHY .\nginx sometimes, OTHERWISE NOT?******
-s signal     : send signal to a master process: stop, quit, reopen, reload
--> No signal without process being started first


******HTML FILE******
If you want to edit the default HTML file on port 8123:
--> ***edit this***: <path_to_nginx>\html\index.html (on Windows)
