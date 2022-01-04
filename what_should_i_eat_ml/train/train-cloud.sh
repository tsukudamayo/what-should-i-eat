#!/bin/bash
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# This script performs cloud training for a PyTorch model.

echo "Submitting PyTorch model training job to Vertex AI"

PROJECT_ID=systemt-331700
BUCKET_NAME=what-should-i-eat
JOB_PREFIX="what-should-i-eat-model"
JOB_NAME=${JOB_PREFIX}-$(date +%Y%m%d%H%M%S)-custom-job
REGION="asia-northeast1"
JOB_DIR=gs://${BUCKET_NAME}/${JOB_PREFIX}/models/${JOB_NAME}
IMAGE_REPO_NAME=pytorch-gpu-train-what-should-i-eat
IMAGE_TAG=latest
CUSTOM_TRAIN_IMAGE_URI=gcr.io/${PROJECT_ID}/${IMAGE_REPO_NAME}:${IMAGE_TAG}
docker build --no-cache -f Dockerfile -t $CUSTOM_TRAIN_IMAGE_URI .
# docker build -f Dockerfile -t $CUSTOM_TRAIN_IMAGE_URI .
docker push ${CUSTOM_TRAIN_IMAGE_URI}
gcloud beta ai custom-jobs create \
    --display-name=${JOB_NAME} \
    --region ${REGION} \
    --worker-pool-spec=replica-count=1,machine-type='n1-standard-4',accelerator-type='NVIDIA_TESLA_T4',accelerator-count=1,container-image-uri=${CUSTOM_TRAIN_IMAGE_URI} \
    --args="--model-name","what-should-i-eat","--job-dir",$JOB_DIR

echo "After the job is completed successfully, model files will be saved at $JOB_DIR/"
