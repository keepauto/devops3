{% for app in apps %}
    upstream {{ %app["name"] %}} {
       {{% for up in app["upstream"] %}} 
            server {{ up["host"] }}:{{ up["port"] }}; 
       {{% endfor %}} 
    }   
{% endfor %}

    server {
        listen 808 
        server_name reboot.linrc.com
      {% for app in apps %}
        location /{{ app["name"] }} { 
            proxy_pass http://{{ app["name"] }}; 
        }   
      {% endfor %}
    }   
