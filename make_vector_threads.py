from multiprocessing import Process
from tqdm import tqdm
from time import time
import uuid
import random
from nltk.corpus import words

textos = []
#uuid genera un id de 16 bytes unico para cada palabra
def hash_gen (in_word, frec):
    idu = uuid.uuid5(uuid.NAMESPACE_DNS, in_word)
    str_bin = ""
    for h in idu.bytes:
        str_bin += format(h, '#010b')[2:]#quito lo no binario
    int_bin = []
    for sb in str_bin:
        int_bin += [int(sb)]
    for i in range(len(int_bin)):
        if int_bin[i] == 1:
            int_bin[i]+= frec
        else:
            int_bin[i]-= frec
    return int_bin

def text_generator (my_dict, len_words):
    text = ""
    for i in range(len_words):
        text += my_dict[random.randint(0, len(my_dict)-1)]+" "
    return text

def sim_hash_gen (in_words):
    dic_text = {}
    for w in in_words.split(" ")[:-1]:
        if w in dic_text:
            dic_text[w] += 1
        else:
            dic_text[w] = 1
    matrix_hash = []
    for wd in dic_text:
        matrix_hash += [hash_gen(wd,dic_text[wd])]
    return matrix_hash

def sum_matrix (matrix):
    vector_out = [0]*len(matrix[0])
    for v in range(len(matrix)):
        for i in range(len(matrix[0])):
            vector_out[i] += matrix[v][i]
    for b in range(len(vector_out)):
        if vector_out[b] <= 0:
            vector_out[b] = '0'
        else:
            vector_out[b] = '1'
    return "".join(vector_out)

def exe_thread (t,num,part_text):
    for i,text in enumerate(part_text):
        sim_hash = sum_matrix(sim_hash_gen (text))
        print (str((t*num)+i)+'\t'+sim_hash)

def main():
    #500 terminos
    my_dictionary = words.words()[10::474]
    #numero de textos
    n_text = 2560
    #Cantidad de palabras por texto
    long_text = 4000
    
    global textos
    
    start = time()
    for i in tqdm(range(n_text)):
        textos += [text_generator (my_dictionary,long_text)]
    print ("Time of Text Generator:",time()-start,"seg")

    start = time()
    for t in tqdm(range(n_text)):
        sum_matrix(sim_hash_gen (textos[t]))
    time_linear = time()-start
    print ("All Time Linear:",time_linear,"seg",int(n_text*long_text/time_linear),"Word/s")

    n_thread = 1

    texts4thread = int(n_text/n_thread)
    n_count = 0
    
    pos = 0
    threads = []

    time_all = time()
    for i in range(n_thread):
        t = Process(target=exe_thread, args=(i,texts4thread,textos[pos:pos+texts4thread],))
        print ("Start Thread:",i+1)
        t.start()
        threads.append(t)
        pos += texts4thread
    print ("Time of Start Thread:",time()-time_all,"seg")

    time_end = time()
    for i,t in enumerate(threads):
        t.join()
        print ("Finish Thread:",i+1)

    print ("Time of End Thread:",time()-time_end,"seg")

    time_thread = time()-time_all
    print ("All Time Thread:",time_thread,"seg,",int(n_text*long_text/time_thread),"Word/s")


if __name__ == "__main__":
    main()

