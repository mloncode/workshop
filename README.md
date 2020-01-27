# Machine Learning for Software Engineering: modelling the source code

Slides are [online](https://mlonco.de/workshop/).

OSS tools covered:

- [gitbase](https://docs.sourced.tech/gitbase)
- [bblfsh](https://doc.bblf.sh)
- [BigARTM](http://bigartm.org)
- [PyTorch](https://pytorch.org)

 <details>
<summary>Abstract</summary>

> Machine Learning on Source Code (MLonCode) is an emerging research domain which stands at the intersection of deep learning, natural language processing, software engineering and programming language communities.
>
> During this 3h30 workshop, we will review recent Software Engineering tasks that benefit from applying Machine Learning, with a focus on hands-on experience on:
> - extracting data from real source code
> - developing multiple Machine Learning models
> - for a particular task of source code summarization (or function name suggestion).
>
> At the end of the workshop participants will build 2 working models on a real dataset, producing near state-of-the-art results. Practical skill of extracting information from source code as well as modelling different aspects of it are going to be acquired.
>
> Prerequisites: familiarity with the basics of DeepLearning, a laptop with Docker installed

</details>

## Prerequisites

- Docker

## Dependencies

Import Docker images (works offline):

```
docker load -i images/jupyter.tgz
docker load -i images/gitbase.tgz
docker load -i images/bblfshd-with-drivers.tgz

docker images
```

Run bblfsh

```shell
docker run \
    --detach \
    --rm \
    --name amld_bblfshd \
    --privileged \
    --publish 9432:9432 \
    bblfsh/bblfshd:v2.15.0-drivers \
    --log-level DEBUG
```

Run gitbase

```shell
docker run \
    --detach \
    --rm \
    --name amld_gitbase \
    --publish 3306:3306 \
    --link amld_bblfshd:amld_bblfshd \
    --env BBLFSH_ENDPOINT=amld_bblfshd:9432 \
    --env MAX_MEMORY=1024 \
    --volume $(pwd)/repos/git-data:/opt/repos \
    srcd/gitbase:v0.24.0-rc2
```

Run the jupyter image

```shell
docker run \
    --rm \
    --name amld_jupyter \
    --publish 8888:8888 \
    --link amld_bblfshd:amld_bblfshd \
    --link amld_gitbase:amld_gitbase \
    --volume $(pwd)/notebooks:/amld/notebooks \
    --volume $(pwd)/repos:/amld/repos \
    mloncode/amld
```

<details>
<summary>With make</summary>

To build the workshop image and launch the 3 required containers

```shell
make build-and-run
```

To only launch the 3 required containers

```shell
make
```

</details>

## Workflow

### 1. Download the data

We are going to use top 50 repositories from [Apache Software Foundation](https://www.apache.org) though this workshop.

[Notebook 1: data collection pipeline](http://127.0.0.1:8888/notebooks/Download%20repositories.ipynb) ([example](notebooks/Download%20repositories.ipynb))

### 2. Project and Developer Similarities

Build a vector model for projects and developers using [Topic Modelling](https://en.wikipedia.org/wiki/Topic_model) of code identifiers.

[Notebook 2: project and developer similarities](http://127.0.0.1:8888/notebooks/Project%20and%20Developer%20Similarity.ipynb) ([example](notebooks/Project%20and%20Developer%20Similarity.ipynb))

### 3. Function Name Suggestion

Train a NMT [seq2seq model](https://towardsdatascience.com/nlp-sequence-to-sequence-networks-part-2-seq2seq-model-encoderdecoder-model-6c22e29fd7e1) for predicting method names based on identifiers in method bodies.

[Notebook 2: function name suggestion](http://127.0.0.1:8888/notebooks/Name%20suggestion.ipynb) ([example](notebooks/Name%20suggestion.ipynb))
