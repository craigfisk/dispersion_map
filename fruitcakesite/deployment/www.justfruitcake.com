server {
    listen       80;
    server_name  justfruitcake.com www.justfruitcake.com;
##    root /var/www/www.justfruitcake.com;
##    index index.html;
    charset utf-8;
	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

    location / {
        include     /etc/nginx/uwsgi_params;
        uwsgi_pass unix:///tmp/uwsgi.sock;  
        # remember to change to a cluster if > 1 uwsgi app
#        include uwsgi_params
#        uwsgi_pass  127.0.0.1:9001;

        allow 70.102.23.162;
        allow 67.168.194.54;
        allow 75.93.45.221; 
        allow 98.232.246.175;  
        deny all;
      # serve static files that exist w/o running other rewrite tests
		if (-f $request_filename) {
			expires 30d;
			break;
		}
    }
    location = /robots.txt { log_not_found off; access_log off;  }
    location = /favicon.ico {access_log off; log_not_found off; }
    location ~* \.(jpg|jpeg|png|gif|css|js|ico)$ { expires max; access_log off;  log_not_found off;  }

    location /static {
        root /home/fisk/virt/justfruitcake/fruitcakesite/static/;
    }
    location /media {
        root /home/fisk/virt/justfruitcake/fruitcakesite/static/media/;
    }
#    location ~ \.py$ {
#        uwsgi_pass unix:///tmp/uwsgi.sock;
#        include /usr/local/nginx/conf/uwsgi_params;
#    }

# nginx documentation example http://wiki.nginx.org/HttpUwsgiModule also discusses directives:
# location / {
#     include uwsgi_params;
#     uwsgi_pass unix:/var/run/example.com.sock;
#}
# django with nginx + uwsgi:  http://www.westphahl.net/blog/2010/4/8/running-django-nginx-and-uwsgi/



}

