import csv
import sys


def main():

    pos_reviews = []
    neg_reviews = []


    file1 = open('yelp_labelled.csv', 'r', newline='') 
    reader2 = csv.DictReader(file1)

    for line in reader2:
        if line["label"] == '1':
                pos_reviews.append(line["review"])
        else:
            neg_reviews.append(line["review"])
    file1.close()


    print("Positive Reviews:")
    print(pos_reviews[:5])

    print("Negative reviews:")
    print(neg_reviews[:5])

    print( "Total Negative Reviews:",len(neg_reviews))
    print("Total Positive Reviews:",len(pos_reviews))\

    neg_bag_words = [ neg_review.split() for neg_review in neg_reviews]
    pos_bag_words = [ pos_review.split() for pos_review in pos_reviews]



    pos_voc = pos_bag_words[0]
    for bag_words in  pos_bag_words[1:]:
        pos_voc += bag_words
    neg_voc = neg_bag_words[0]
    for bag_words in  neg_bag_words[1:]:
        neg_voc += bag_words


    vocab = pos_voc + neg_voc


    print("Vocabulary: ")
    print(vocab[:6])

    positives = len(pos_reviews)
    negatives = len(neg_reviews)

    total = len(neg_reviews) + len(pos_reviews)

    Hash = {}

    for word in vocab:
        in_pos_reviews = 1
        in_neg_reviews = 1
        for review in pos_bag_words:
            if word in review:
                in_pos_reviews += 1
        for review in neg_bag_words:
            if word in review:
                in_neg_reviews += 1  
        
        pos_prob = in_pos_reviews/positives
        neg_prob = in_neg_reviews/negatives
        Hash[word] = {"positive": pos_prob , "negative":neg_prob }


    pos = positives / total
    neg = negatives / total

    


    base_pos_prob = 1/349
    base_neg_prob = 1/643

    if len(sys.argv) == 1:

        sentence = input("Enter the Review: ")
        review = sentence.split()
        positive_prob = pos
        negative_prob = neg
        for word in review:
            if word in Hash:
                positive_prob *= Hash[word]["positive"]
                negative_prob *= Hash[word]["negative"]
            else:
                positive_prob *= base_pos_prob
                negative_prob *= base_neg_prob
                

        #Normalize
        total = positive_prob + negative_prob
        positive_prob =  positive_prob / total
        negative_prob =  negative_prob / total
        print(sentence)
        print(f"probability the review is positive: {positive_prob:.4f}") 
        print(f"probability the review is negative: {negative_prob:.4f}")
        print()


    if len(sys.argv) == 2:

        print("-------Testing New Reviews-------", "\n")

        test = open('Test.txt', 'r').read().splitlines()
        for sentence in test:
            review = sentence.split()
            positive_prob = pos
            negative_prob = neg
            for word in review:
                if word in Hash:
                    positive_prob *= Hash[word]["positive"]
                    negative_prob *= Hash[word]["negative"]
                else:
                    positive_prob *= base_pos_prob
                    negative_prob *= base_neg_prob
                    

            #Normalize
            total = positive_prob + negative_prob
            positive_prob =  positive_prob / total
            negative_prob =  negative_prob / total
            #print(sentence)
            if positive_prob > 0.50:
                return f"probability the review is positive: {positive_prob:.4f}"
            else:
               return f"probability the review is negative: {negative_prob:.4f}"
            

main()

