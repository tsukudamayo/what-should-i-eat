# Dockerfile to build custom container for training
# use PyTorch DLVM as base image
FROM gcr.io/cloud-aiplatform/training/pytorch-gpu.1-7

WORKDIR /root/app
RUN mkdir ../input

# installs transformers, datasets and google-cloud-storage sdk
RUN pip install \
    google-cloud-storage \
    transformers \
    fugashi \
    ipadic \
    sentence_transformers

# Copies the trainer code to the docker image.
COPY ./__init__.py ./__init__.py
COPY ./models.py ./models.py
COPY ./input/dislikes_recipe.tsv ../input/dislikes_recipe.tsv
COPY ./input/likes_recipe.tsv ../input/likes_recipe.tsv

# Set up the entry point to invoke the trainer.
ENTRYPOINT ["python", "models.py"]
