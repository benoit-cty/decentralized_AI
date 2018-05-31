# decentralized_AI

This is a first try at building a Decentralized AI.

## Building the Docker Image

```
docker build docker_keras_cpu/ -t trancept/keras_mnist:v0
docker run -v /tmp:/iexec trancept/keras_mnist:v0
docker push trancept/keras_mnist:v0
```

=> It will train an AI to do OCR on the well known MNIST dataset.
Dockerfile is based on work from https://github.com/gw0/docker-keras , thanks to him.

## Adding docker image to iExec

- Edit iexec.js
- Run
```
iexec app deploy
iexec app show
$ iexec order init --buy
ℹ using chain [kovan]
✔ Saved default order in "iexec.json", you can edit it:
app:     0xf0e67cfc243801f78abe21e0704a9e8c31cff703
dataset: 0x0000000000000000000000000000000000000000
params: 
  cmdline: --help
ben@rig:~/src/decentralized_AI$ iexec order place
✖ command "iexec order place" failed with Error: Missing order. You probably forgot to run "iexec order init --sell"
```

=> So it's a Fail for now.
