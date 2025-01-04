from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
#import subprocess
#import os
import csv
from collections import Counter, defaultdict

def analyze_review(request):
    if request.method == "POST":
        review = request.POST.get("review")
        result = run_sentiment_analysis(review)
        sentiment = result
        return render(request, 'result.html', {'sentiment': sentiment , "rev":review ,"ret":result})
    return render(request, 'review_form.html')

def run_sentiment_analysis(review):
    # Initialize lists for positive and negative reviews
    pos_reviews = []
    neg_reviews = []

    # Load data from CSV file
    with open('yelp_labelled.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for line in reader:
            if line["label"] == '1':
                pos_reviews.append(line["review"])
            else:
                neg_reviews.append(line["review"])

    # Handle empty review datasets
    if len(pos_reviews) == 0 or len(neg_reviews) == 0:
        return "neutral"  # or another fallback

    # Build bag-of-words model
    pos_bag_words = [word for review in pos_reviews for word in review.split()]
    neg_bag_words = [word for review in neg_reviews for word in review.split()]

    # Count word frequencies in positive and negative reviews
    pos_word_counts = Counter(pos_bag_words)
    neg_word_counts = Counter(neg_bag_words)

    # Calculate vocabulary and prior probabilities
    vocab = set(pos_word_counts.keys()).union(neg_word_counts.keys())
    total_pos_reviews = len(pos_reviews)
    total_neg_reviews = len(neg_reviews)
    total_reviews = total_pos_reviews + total_neg_reviews

    # Handle zero division in prior probabilities
    if total_reviews == 0:
        return "neutral"  # or another fallback

    pos_prior = total_pos_reviews / total_reviews
    neg_prior = total_neg_reviews / total_reviews

    # Calculate probabilities for each word with Laplace smoothing
    word_probs = defaultdict(lambda: {"positive": 1 / (total_pos_reviews + 1), 
                                      "negative": 1 / (total_neg_reviews + 1)})

    for word in vocab:
        word_probs[word]["positive"] = (pos_word_counts[word] + 1) / (len(pos_bag_words) + len(vocab))
        word_probs[word]["negative"] = (neg_word_counts[word] + 1) / (len(neg_bag_words) + len(vocab))

    # Classify the given review
    words_in_review = review.split()
    pos_prob = pos_prior
    neg_prob = neg_prior

    for word in words_in_review:
        # Make sure word exists in word_probs
        if word in word_probs:
            pos_prob *= word_probs[word]["positive"]
            neg_prob *= word_probs[word]["negative"]
        else:
            # Handle unseen words (default to smoothing)
            pos_prob *= 1 / (len(pos_bag_words) + len(vocab))
            neg_prob *= 1 / (len(neg_bag_words) + len(vocab))

    # Normalize probabilities
    total_prob = pos_prob + neg_prob
    pos_prob /= total_prob
    neg_prob /= total_prob

    # Determine sentiment based on probabilities
    if 0.45 <= pos_prob <= 0.55 and 0.45 <= neg_prob <= 0.55:
        return "neutral"
    elif pos_prob > neg_prob:
        return "positive"
    else:
        return "negative"




# def run_sentiment_analysis(review):
#     # Initialize lists for positive and negative reviews
#     pos_reviews = []
#     neg_reviews = []

#     # Load data from CSV file
#     with open('yelp_labelled.csv', 'r', newline='') as file:
#         reader = csv.DictReader(file)
#         for line in reader:
#             if line["label"] == '1':
#                 pos_reviews.append(line["review"])
#             else:
#                 neg_reviews.append(line["review"])

#     # Build bag-of-words model
#     pos_bag_words = [word for review in pos_reviews for word in review.split()]
#     neg_bag_words = [word for review in neg_reviews for word in review.split()]

#     # Count word frequencies in positive and negative reviews
#     pos_word_counts = Counter(pos_bag_words)
#     neg_word_counts = Counter(neg_bag_words)

#     # Calculate vocabulary and prior probabilities
#     vocab = set(pos_word_counts.keys()).union(neg_word_counts.keys())
#     total_pos_reviews = len(pos_reviews)
#     total_neg_reviews = len(neg_reviews)
#     total_reviews = total_pos_reviews + total_neg_reviews

#     pos_prior = total_pos_reviews / total_reviews
#     neg_prior = total_neg_reviews / total_reviews

#     # Calculate probabilities for each word
#     word_probs = defaultdict(lambda: {"positive": 1 / (total_pos_reviews + 1), 
#                                       "negative": 1 / (total_neg_reviews + 1)})

#     for word in vocab:
#         word_probs[word]["positive"] = (pos_word_counts[word] + 1) / (len(pos_bag_words) + len(vocab))
#         word_probs[word]["negative"] = (neg_word_counts[word] + 1) / (len(neg_bag_words) + len(vocab))

#     # Classify the given review
#     words_in_review = review.split()
#     pos_prob = pos_prior
#     neg_prob = neg_prior

#     for word in words_in_review:
#         pos_prob *= word_probs[word]["positive"]
#         neg_prob *= word_probs[word]["negative"]

#     # Normalize probabilities
#     total_prob = pos_prob + neg_prob
#     pos_prob /= total_prob
#     neg_prob /= total_prob

#     # Determine sentiment based on probabilities
#     if 0.45 <= pos_prob <= 0.55 and 0.45 <= neg_prob <= 0.55:
#         return "neutral"
#     elif pos_prob > neg_prob:
#         return "positive"
#     else:
#         return "negative"

    """  
    #Save review temporarily to a file
    temp_file = "temp_review.txt"
    with open(temp_file, "w") as file:
        file.write(review)
    
    # Run Sentiment.py and capture the output
    try:
        process = subprocess.run(
            ['python', 'Sentiment.py', temp_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = process.stdout.lower()
        if "positive" in output:
            return "positive"
        return "negative"
    finally:
        # Clean up temporary file
        os.remove(temp_file)
    """