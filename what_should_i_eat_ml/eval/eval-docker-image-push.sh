PROJECT_ID=systemt-331700
IMAGE_REPO_NAME=pytorch-gpu-eval-what-should-i-eat
IMAGE_TAG=latest
CUSTOM_EVAL_IMAGE_URI=gcr.io/${PROJECT_ID}/${IMAGE_REPO_NAME}
docker build --tag=${CUSTOM_EVAL_IMAGE_URI} .
