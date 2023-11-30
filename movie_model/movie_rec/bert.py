import time
from transformers import TFAutoModel, AutoTokenizer
import numpy as np

# download hugging face models
MODEL = TFAutoModel.from_pretrained('bert-base-uncased')
BATCH_SIZE= 1
MAX_LENGTH = 60
MODEL_TYPE = 'bert-base-uncased'
# loading the model with its weigths



def bert_inp_fct(sentences, bert_tokenizer, max_length) :
    """
    Preprocessing Text function
    From :
      sentences : list
      bert_tokenizer : transformers.AutoTokenizer
      max_lenght : int | the maximum length to use by one of the truncation/padding parameters

    Return :
      input_ids, token_type_ids, attention_mask, bert_inp_tot  : np.array

    """
    # --- Output Explanation ------------------------------------------------------
    #
    # Input Ids
    #
    #  List of token ids to be fed to a model ( words real embeddings)
    input_ids=[]
    #
    #
    # Token Type ids ( segment embeddings )
    #
    # The token type ids(pairing and keeping a way to identify the response and the question)
    # The first sequence, the “context” used for the question(if any), has all its tokens represented by a 0,
    # whereas the second sequence, corresponding to the “question”, has all its tokens represented by a 1.
    # In short : It is binary mask identifying the two types of sequence in the model.
    #
    #
    token_type_ids = []
    #
    # Attention Mask
    #
    # The attention mask is a binary tensor indicating the position of the padded indices
    # so that the model does not attend to them. For the BertTokenizer
    # 1 indicates a value that should be attended to, while 0 indicates a padded value.
    attention_mask=[]
    #
    # -----------------------------------------------------------------------------
    # USELESS  but keeping it for legacy
    bert_inp_tot = []

    #---- Tokenizing each sentence ---------------------------------------------------
    for sent in sentences:
        
        # Converts a string to a sequence of ids (integer), using the tokenizer and vocabulary.
        bert_inp = bert_tokenizer.encode_plus(sent,
                                              add_special_tokens = True,
                                              max_length = max_length,
                                              padding='max_length',
                                              return_attention_mask = True,
                                              return_token_type_ids=True,
                                              truncation=True,
                                              return_tensors="tf")

        # appending the values to their  containers
        input_ids.append(bert_inp['input_ids'][0])
        token_type_ids.append(bert_inp['token_type_ids'][0])
        attention_mask.append(bert_inp['attention_mask'][0])
        bert_inp_tot.append((bert_inp['input_ids'][0],
                             bert_inp['token_type_ids'][0],
                             bert_inp['attention_mask'][0]))

    # type conversion into numpy
    input_ids = np.asarray(input_ids)
    token_type_ids = np.asarray(token_type_ids)
    attention_mask = np.array(attention_mask)

    return input_ids, token_type_ids, attention_mask, bert_inp_tot


# Fonction de création des features
def feature_BERT_fct(model, model_type, sentences, max_length, b_size, mode='HF') :
    """
    Get the output of the given bert model
    From :
      model : transformers.models.bert.modeling_tf_bert.TFBertModel
      model_type : str
      sentences : list
      max_length : int
      b_size : int
      mode : str : HF or TFhub
    Return :
      features_bert :  np.array
      last_hidden_state_tot : np.array
    """
    # it points to the same object so irrelevant however they might be different in some cases ?
    # hence performing operation on one of them
    batch_size = b_size
    batch_size_pred = b_size

    # instantiating this modelètype's tokenizer
    bert_tokenizer = AutoTokenizer.from_pretrained(model_type)
    time1 = time.time()

    #---Predict by batch_size -------------------------------------------------------------------------
    for step in range(len(sentences)//batch_size) :
        
        idx = step*batch_size # retrieving the index

        # ---Preprocess---
        input_ids, token_type_ids, attention_mask, bert_inp_tot = bert_inp_fct(sentences[idx:idx+batch_size],
                                                                      bert_tokenizer, max_length)

        # ---Model mode's---
        #
        #  Bert HuggingFace
        if mode=='HF' :
            # predicting returning
            outputs = model.predict([input_ids, attention_mask, token_type_ids], batch_size=batch_size_pred)
            last_hidden_states = outputs.last_hidden_state

        # # Bert Tensorflow Hub
        if mode=='TFhub' :
            # to dict
            text_preprocessed = {"input_word_ids" : input_ids,
                                 "input_mask" : attention_mask,
                                 "input_type_ids" : token_type_ids}
            outputs = model(text_preprocessed)
            last_hidden_states = outputs['sequence_output']

        # ---Step's output---
        if step == 0 :

            last_hidden_states_tot = last_hidden_states
            last_hidden_states_tot_0 = last_hidden_states
        else :
            # concat the sequence output form step 0 and the last step
            last_hidden_states_tot = np.concatenate((last_hidden_states_tot,last_hidden_states))
    # mean of the concatenated
    features_bert = np.array(last_hidden_states_tot).mean(axis=1)

    time2 = np.round(time.time() - time1,0)
    print("temps traitement : ", time2)

    return features_bert, last_hidden_states_tot

#---PREPROCESS-----------------------------------------------------------------------------------------------------------------

def preprocess(description:list, MODEL, MAX_LENGTH, MODEL_TYPE, BATCH_SIZE):
    """
    preprocess wrapper
    """
    features_bert, last_hidden_states_tot = feature_BERT_fct(MODEL, MODEL_TYPE, description,
                                                         MAX_LENGTH, BATCH_SIZE, mode='HF')
    
    return features_bert


