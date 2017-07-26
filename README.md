### Add Server
```
ssh-keygen -t rsa
ssh <user>@<ip> "mkdir .ssh"
ssh <user>@<ip> "echo \"`cat ~/.ssh/id_rsa.pub`\" >> ~/.ssh/authorized_keys"
./manage.py shell
>>> from main.models import Server
>>> s = Server(ip='<ip>')
>>> s.save()
```

