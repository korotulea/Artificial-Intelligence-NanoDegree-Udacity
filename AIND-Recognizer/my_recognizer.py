import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    word_tmp_X_lengths =  test_set.get_all_Xlengths()
    # iterate each word in the test_set
    for word_tmp in word_tmp_X_lengths:
        X_tmp, lengths_tmp = word_tmp_X_lengths[word_tmp] #test_set.get_item_Xlengths(word_tmp)
        #iterate words in the models and compute probabilities for each word
        prob_tmp_dic = {}
        for model_tmp in models:
            try:
                logL_tmp = models[model_tmp].score(X_tmp, lengths_tmp)
            except:
                logL_tmp = - float("inf")
            prob_tmp_dic[model_tmp] = logL_tmp
        # find the key in prob_tmp_dic for the max value of logL
        word_best = max(prob_tmp_dic, key=prob_tmp_dic.get)
        guesses.append(word_best)   
        probabilities.append(prob_tmp_dic)
    return probabilities, guesses

