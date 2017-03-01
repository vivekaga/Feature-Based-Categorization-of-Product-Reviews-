# Feature-Based-Categorization-of-Product-Reviews
This project is an implementation of Machine Learning and Natural Language Processing to identify the important features of a product being reviewed by the customers and its corresponding sentiment. This is a sample of a larger web-application which maintains a MongoDB database to store collections of most popular features being talked about (Trending Features) and performs analysis of the user satisfaction regarding each feature.

This sample module is the backend algorithm which consists of a Natural Language Parser, Grammer for state machine and pickle files for 'pre-trained' parts-of-speech tagger, stopwords-identifier and sentiment classifier. A pickle file is a binary file which consists of the meta-data obtained by training a classifier through a training set. The importance of pickle file is that it can be reused each time you run the algorithm without having to re-train the classifiers, thereby improving efficiency and reducing completion time.

<h1> File Structure </h1>
1. parser.py : Consists of the parsing algorithm and also performs sentimental analysis and displays final result on std output.
2. classifier.pkl : Binary file consisting of a meta data for Naive Bayes Classifier.
3. stopwords.pkl : Binary file consisting of meta data for Stop Words Classifier.
4. tagger.pkl : Binary file consisting of meta data for parts-of-speech tagger.
5. sample.txt : Consists of "pre-processed" (all lowercase, no special characters or numbers) product reviews for analysis.

<h1> How to run? </h1>
1. Clone the project and ensure all files are in same folder.
2. Input sample "pre-processed" reviews of a product in sample.txt
3. Run and excute the parser.py file.
4. Obtain detailed feature based sentiment classification result on std output. (This is a sample where "pos" indicates positive sentiment and "neg" indicates negative sentiment corresponding to each feature identified in the review.)

