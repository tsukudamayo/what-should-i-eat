#!/bin/bash
REGION=asia-northeast1

# set job name
JOB_NAME=what-should-i-eat-model-20220104191934-custom-job

# get job id
JOB_ID=$(gcloud beta ai custom-jobs list --region=$REGION --filter="displayName:"$JOB_NAME --format="get(name)")

# get model artifacts directory location set when running the training job
GCS_MODEL_ARTIFACTS_URI=$(gcloud beta ai custom-jobs describe $JOB_ID --region=$REGION --format="get(jobSpec.baseOutputDirectory.outputUriPrefix)")

# download model artifacts from GCS to a local directory
gsutil -m cp -r $GCS_MODEL_ARTIFACTS_URI/models ./
