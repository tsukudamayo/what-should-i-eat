#!/bin/bash
REGION=asia-northeast1

# set job name
JOB_NAME=what-should-i-eat-model-20220105035116-custom-job
# get job id
JOB_ID=$(gcloud beta ai custom-jobs list --region=$REGION --filter="displayName:"$JOB_NAME --format="get(name)")

# get model artifacts directory location set when running the training job
#GCS_MODEL_ARTIFACTS_URI=$(gcloud beta ai custom-jobs describe $JOB_ID --region=$REGION --format="get(jobSpec.baseOutputDirectory.outputUriPrefix)")
GCS_MODEL_ARTIFACTS_URI=gs://what-should-i-eat/what-should-i-eat-model/models/20220104103356-custom-job

# download model artifacts from GCS to a local directory
gsutil -m cp -r $GCS_MODEL_ARTIFACTS_URI/ ./models
