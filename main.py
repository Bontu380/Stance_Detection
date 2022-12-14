# -*- coding: utf-8 -*-
import Models
import Util

# Data that are tagged with 2016 belong to SemEval[1] dataset whereas 2020 data belong to P-stance[2] dataset.

# [1] S. Mohammad, S. Kiritchenko, P. Sobhani, X. Zhu, C. Cherry, ‘Semeval2016 task 6: Detecting stance in tweets’,
#    Proceedings of the 10th international workshop on semantic evaluation (SemEval-2016), 2016, . 31–41.

# [2] Y. Li, T. Sosea, A. Sawant, A. J. Nair, D. Inkpen, C. Caragea, ‘P-stance: A large dataset for stance detection
#    in political domain’, Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021, . 2355–2365.

glove_path = "GloVe_Embeddings/glove.twitter.27B.200d.txt"

trump_train_2020 = "Pstance/raw_train_trump.csv"
biden_train_2020 = "Pstance/raw_train_biden.csv"
bernie_train_2020 = "Pstance/raw_train_bernie.csv"

hillary_val_2016 = "SemEval2016/hillary_validation.csv"
trump_val_2020 = "Pstance/raw_val_trump.csv"
biden_val_2020 = "Pstance/raw_val_biden.csv"
bernie_val_2020 = "Pstance/raw_val_bernie.csv"

hillary_test_2016 = "SemEval2016/hillary_test.csv"
trump_test_2016 = "SemEval2016/SemEval2016-Task6-subtaskB-testdata-gold.txt"

trump_test_2020 = "Pstance/raw_test_trump.csv"
biden_test_2020 = "Pstance/raw_test_biden.csv"
bernie_test_2020 = "Pstance/raw_test_bernie.csv"

#######################################################################  CROSS TARGET  ##########################################################################

# In the cross-target stance detection task, we train and test our model on different combinations of politicans' data.

X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[biden_train_2020],val=[hillary_val_2016],test=[hillary_test_2016]) #Biden => Hillary
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[bernie_train_2020],val=[hillary_val_2016],test=[hillary_test_2016]) #Bernie => Hillary
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length =  Util.get_data(train=[trump_train_2020],val=[hillary_val_2016],test=[hillary_test_2016]) #Trump => Hillary
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[trump_train_2020],val=[biden_val_2020],test=[biden_test_2020]) #Trump => Biden
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[trump_train_2020],val=[bernie_val_2020],test=[bernie_test_2020]) #Trump => Bernie
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[biden_train_2020],val=[trump_val_2020],test=[trump_test_2020]) #Biden => Trump
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[biden_train_2020],val=[bernie_val_2020],test=[bernie_test_2020]) #Biden => Bernie
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[bernie_train_2020],val=[trump_val_2020],test=[trump_test_2020]) #Bernie => Trump
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[bernie_train_2020],val=[biden_val_2020],test=[biden_test_2020]) #Bernie => Biden
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[trump_train_2020,biden_train_2020],val=[bernie_val_2020],test=[bernie_test_2020]) #Trump & Biden => Bernie
#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[trump_train_2020,bernie_train_2020],val=[biden_val_2020],test=[biden_test_2020]) #Trump & Bernie => Biden
#X_train, y_train, X_validation, y_validation, X_test, y_test, word_dict, max_length = Util.get_data(train=[biden_train_2020, bernie_train_2020], val=[trump_val_2020], test=[trump_test_2020])  # Biden & Bernie => Trump

#######################################################################  CROSS TOPIC  ##########################################################################

# We aim to train our model with P-stance Donald Trump
# dataset and test it on SemEval2016 Donald Trump dataset. To compare our
# results with the results in [2], we also do not take the tweets with
# ”neutral” label into consideration thus we will classify the tweets as ”Favor”
# and ”Against”.

#X_train,y_train,X_validation,y_validation,X_test,y_test,word_dict,max_length = Util.get_data(train=[trump_train_2020],val=[trump_val_2020],test=[trump_test_2020]) #Trump 2020 => Trump 2020, this line is not cross topic but included for
# comparison.

#X_train, y_train, X_validation, y_validation, X_test, y_test, word_dict, max_length = Util.get_data(train=[trump_train_2020],
#                                                                                               val=[trump_val_2020],
#                                                                                               test=[trump_test_2016])  # Trump 2020 => Trump 2016, cross topic.


print("Train_X: " + str(X_train.shape) + " Val_X: " + str(X_validation.shape) + " Test_X: " + str(X_test.shape))
print("Train_y: " + str(y_train.shape) + " Val_y: " + str(y_validation.shape) + " Test_y: " + str(y_test.shape))
################################################################################################################################################


# Prepare embedding matrix where each row represents a word embedding, a [vocab_size x embedding dimension] size matrix.
vocab_size = len(word_dict) + 1
glove_embeddings_dict, embedding_dim = Util.load_glove_vectors(glove_path,word_dict)  # If a word occurs in t.word_index dictionary, then we will have its embedding in glove_embeddings dict.
embedding_matrix = Util.create_embedding_matrix(glove_embeddings_dict, vocab_size, embedding_dim, word_dict)

# Get model.
#model = Models.get_Kims_model_original(vocab_size,embedding_dim,embedding_matrix,max_length) #Kim's original
model = Models.get_Kims_model_updated(vocab_size, embedding_dim, embedding_matrix, max_length)  # Model we augmented.

# Train the model.
model.fit(X_train, y_train, validation_data=(X_validation, y_validation), batch_size=256, epochs=100, verbose=1)


# Test the model.
model.evaluate(X_test, y_test, verbose=1)
