# tae reddit bot and web experiment

## [Youtube video](https://youtu.be/BCWHfPkVinc)

## About

This was a social web experiment which took place in several Turkish meme subreddits between April 18 and May 5 2020. 

Bot imitates r/tamamahbapengelli (and some other similar subs) users by posting comments which generated from a trained [GPT-2](https://openai.com/blog/better-language-models/) unsupervised Transformer language model.

## What I did

I scraped over 3000 comments from r/tae subreddit, filtered them and created a dataset to finetune GPT-2 355M model using [this](https://colab.research.google.com/drive/1qxcQ2A1nNjFudAGN_mcMOnvV9sF_PkEb) example Colab Notebook.

I spent 2 days training/finetuning the model to make it generate better comments (it wasn't very effective). 

Finished writing the bot and made it comment under posts looking as humanly as possible by combining GPT-2 generated text with a human-like bot behaviour (sleeping at night, not commenting to a new post immediatly etc.).

## Notes
Scraped and generated data contains many Turkish and English swearwords (including racist ones). Be cautious if you want to use them. 