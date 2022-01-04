from typing import List, Dict, Optional

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import torch
from torch import Tensor
import torch.nn as nn
from torch.utils.data import DataLoader

import transformers
transformers.BertTokenizer = transformers.BertJapaneseTokenizer
from sentence_transformers import SentenceTransformer
from sentence_transformers import models
from sentence_transformers.losses import TripletDistanceMetric, TripletLoss
from sentence_transformers.evaluation import TripletEvaluator
from sentence_transformers.readers import TripletReader
from sentence_transformers.datasets import SentencesDataset


SEED = 1


def generate_train_data(
    likes_recipe_file: str = "../input/likes_recipe.tsv",
    dislikes_recipe_file: str = "../input/dislikes_recipe.tsv",
) -> None:

    df_dislike = pd.read_csv(
        dislikes_recipe_file,
        delimiter="\t",
        header=None,
        names=["title", "recipe"],
    )
    df_dislike = df_dislike.dropna()
    print("df_dislike : ", len(df_dislike))

    df_like = pd.read_csv(
        likes_recipe_file,
        delimiter="\t",
        header=None,
        names=["title", "recipe"],
    )
    df_like = df_like.dropna()
    print("df_like : ", len(df_like))

    df_like_sample = df_like.sample(frac=1, random_state=SEED)
    df_dislike_sample = df_dislike.sample(frac=1, random_state=SEED)
    print("df_like_sample " , len(df_like_sample))
    print("df_dislike_sample " , len(df_dislike_sample))

    anchor_sample = df_like_sample[:100]
    pos_sample = df_like_sample[100:]
    neg_sample = df_dislike_sample[:100]

    anchor_caption = anchor_sample["recipe"].values
    pos_caption = pos_sample["recipe"].values
    neg_caption = neg_sample["recipe"].values

    print("anchor_caption : ", len(anchor_caption))
    print("pos_caption : ", len(pos_caption))
    print("neg_caption : ", len(neg_caption))

    triplet_train_dataset = pd.DataFrame({
        "anchor": anchor_caption,
        "pos": pos_caption,
        "neg": neg_caption,
    }).reset_index()
    print("triplet_train_dataset : ", len(triplet_train_dataset))

    triplet_train_dataset.to_csv(
        "train.tsv",
        sep="\t",
        index=False,
    )

    return None


def train(train_data: str = "train.tsv") -> None:
    transformer = models.Transformer("cl-tohoku/bert-base-japanese-whole-word-masking")
    pooling = models.Pooling(
        transformer.get_word_embedding_dimension(),
        pooling_mode_mean_tokens=True,
    )
    model = SentenceTransformer(modules=[transformer, pooling])
    triplet_reader = TripletReader(".")
    train_dataset = SentencesDataset(
        triplet_reader.get_examples("train.tsv"),
        model=model,
    )

    BATCH_SIZE = 4
    NUM_EPOCH = 5
    EVAL_STEPS = 1000
    WARMUP_STEPS = int(len(train_dataset) // BATCH_SIZE * 0.1)

    train_dataloader = DataLoader(
        train_dataset,
        shuffle=False,
        batch_size=BATCH_SIZE,
    )
    train_loss = TripletLoss(
        model=model,
        distance_metric=TripletDistanceMetric.EUCLIDEAN,
        triplet_margin=1,
    )

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=NUM_EPOCH,
        evaluation_steps=EVAL_STEPS,
        warmup_steps=WARMUP_STEPS,
        output_path="./sbert",
    )

    return None


def main():
    generate_train_data()
    train()


if __name__ == "__main__":
    main()
