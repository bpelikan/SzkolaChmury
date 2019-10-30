# Zadanie 2

```PowerShell
PS C:\Users\bpelikan> docker images
REPOSITORY                                             TAG                 IMAGE ID            CREATED             SIZE
reservationsystem                                      latest              a6456d131bf6        6 days ago          1.87GB
mslearnazregistrydemobp.azurecr.io/reservationsystem   latest              a6456d131bf6        6 days ago          1.87GB
mcr.microsoft.com/dotnet/core/sdk                      2.2                 f13ac9d68148        2 weeks ago         1.74GB
hello-world                                            latest              fce289e99eb9        9 months ago        1.84kB

PS C:\Users\bpelikan> docker images -aq | foreach {docker rmi -f $_}
Error response from daemon: conflict: unable to delete d111e125798d (cannot be forced) - image has dependent child images
Error response from daemon: conflict: unable to delete 6ed9c22bed0b (cannot be forced) - image has dependent child images
Untagged: reservationsystem:latest
Untagged: mslearnazregistrydemobp.azurecr.io/reservationsystem:latest
Untagged: mslearnazregistrydemobp.azurecr.io/reservationsystem@sha256:219ad972d8fac6b57d80562c3335b563b43f1618a63daa5bb9259dfac31ef96e
Deleted: sha256:a6456d131bf6fc6aa4eccb0c8013195c968792c78a8ed8ad5275fb898caf835f
Deleted: sha256:d111e125798d302712ab57e4f4e8835f7e0991d4e278d4083817878653918d7c
Deleted: sha256:6ed9c22bed0b669756d9d19e4e3d3d21cfc0176d1a53769ddb24c037983a1254
Deleted: sha256:5cd24d5cdb0f9cef76cb5bf8010ba5fbada0e25f21dd25f56dac71ddc43a5dd4
Deleted: sha256:d97a9d395588fa8c0038eef5df6cbe2ab56f32cab42392460088139cecbcff0d
Deleted: sha256:8d0bc59e65801323d3bf39567282527bc1fa5343f50a0fe3c667aaaded7dc3e7
Deleted: sha256:200cdebb5d7fb944ab24a8f91e4ceb4c56583fd9f9f32a122355689afe6114f8
Deleted: sha256:f4f95de779be497338bc1c6597f4f1530056b09d3d2303cf4e6122d5d0d9246b
Deleted: sha256:8dc9d819baf186752d281e6c662cd3c23d30e56f1a3136e83139e1fe92238f94
Deleted: sha256:182086bee4cc069ce5bf6d1aa0c5b860881a43065c18f50ad9c21d1e7ecd4e0e
Deleted: sha256:709c8f3f01f2eeb929d67dd72b1289b7118c15501d31fe3eedae079969884b9c
Deleted: sha256:cd69f20fbc8866aeecd6f71c5969ac2394ac97adf144014f396c6d7614498612
Deleted: sha256:6ca1593c12f57645cbbc1f59593d2a4a165f3012c329fb01034a4a2bc4d8fe1b
Deleted: sha256:b7220a07184bb17ec67286a1c768a6aafb227368a5a551bc1c33855742d7ad59
Deleted: sha256:20be4c10638dec7235af5215eb7c473dcb1e1b59d91bcb69d5c694e2e4ede6ad
Deleted: sha256:ff6124e5c1774f1fd03a91c0be6eec72376694e7db0239d5ed32636a45f79b63
Deleted: sha256:ea7b71666898aee800e30630f28a85762856377a23361dfbc143e7492c4e8e4c
Deleted: sha256:885941051850d36893b42d16236658727ee9ed2323f2cb81d58bcc9d4d774d28
Error: No such image: a6456d131bf6
Error: No such image: 5cd24d5cdb0f
Error: No such image: 8d0bc59e6580
Error: No such image: f4f95de779be
Error: No such image: 709c8f3f01f2
Error: No such image: 8dc9d819baf1
Error: No such image: 20be4c10638d
Error: No such image: 6ca1593c12f5
Error: No such image: ea7b71666898
Untagged: mcr.microsoft.com/dotnet/core/sdk:2.2
Untagged: mcr.microsoft.com/dotnet/core/sdk@sha256:a0e1def091c695ad2c6cd3cdb0359193246a4f8f4093d0030c74ec2a3edc0ae3
Deleted: sha256:f13ac9d681485e127111a1d0c1965128277b07400c6f4bb6108fb6b67ec1b37c
Deleted: sha256:f61881f0177eca3d47a493da5900b4764a2e5b36f45feeed0566dc95c37e8d39
Deleted: sha256:7ed5cbedf879a4bacbaea5b4cd8407bdd26034ad6c21692dd9e97a4531eff472
Deleted: sha256:3dff41d923f938b33374312fddd10de0c42dfc37a11b22f6f41b57efb4fdec59
Deleted: sha256:495986b5af7051a1022da414ebb4222cf696d9bc9b739367d887f2f3c21f9f1b
Deleted: sha256:820a044123a32d277f88c5ba7a9681257ef8888e84a2632c480ef4740f755fc7
Deleted: sha256:c86361c237fd52849714e65437fe952f6256779edbcf1b6723742d3b44a2680d
Deleted: sha256:55e6b89812f369277290d098c1e44c9e85a5ab0286c649f37e66e11074f8ebd1
Untagged: hello-world:latest
Untagged: hello-world@sha256:b8ba256769a0ac28dd126d584e0a2011cd2877f3f76e093a7ae560f2a5301c00
Deleted: sha256:fce289e99eb9bca977dae136fbe2a82b6b7d4c372474c9235adc1741675f587e
Deleted: sha256:af0b15c8625bb1938f1d7b17081031f649fd14e6b233688eea3c5483994a66a3

PS C:\Users\bpelikan> docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
PS C:\Users\bpelikan> docker images -a
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE

PS C:\Users\bpelikan> docker run -t -d nginx /bin/bash
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
b8f262c62ec6: Pull complete
e9218e8f93b1: Pull complete
7acba7289aa3: Pull complete
Digest: sha256:aeded0f2a861747f43a01cf1018cf9efe2bdd02afd57d2b11fcc7fcadc16ccd1
Status: Downloaded newer image for nginx:latest
b5ebc8ca74ffdb9f6b8ee1407f4b2d7b7929337d4321ff38ba5d2344a8e033bc

PS C:\Users\bpelikan> docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
b5ebc8ca74ff        nginx               "/bin/bash"         51 seconds ago      Up 49 seconds       80/tcp              xenodochial_mahavira

PS C:\Users\bpelikan> docker exec -t -i b5ebc8ca74ff /bin/bash
root@b5ebc8ca74ff:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@b5ebc8ca74ff:/# exit
exit

PS C:\Users\bpelikan> docker stop b5ebc8ca74ff
b5ebc8ca74ff
PS C:\Users\bpelikan> docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                     PORTS               NAMES
b5ebc8ca74ff        nginx               "/bin/bash"         4 minutes ago       Exited (0) 7 seconds ago                       xenodochial_mahavira
PS C:\Users\bpelikan> docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```