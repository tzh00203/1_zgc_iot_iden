import math


class EXPLANATION:

    """
        corpus = [
            "What is the weather like today",
            "what is for dinner tonight",
            "this is question worth pondering",
            "it is a beautiful day today",
            " ",
            "",
            "it is a beautiful day Today today today today today today today today SX-XA-IDC-DNS-RECUR-4.163"
        ]
        corpus_id_ip = [
            (1, "123"),
            (2, "123"),
            (3, "123"),
            (6, "123"),
            (10, "123"),
            (23, "123"),
            (39, "123"),
        ]
        :return: { (ip1_id, ip1): [ip1's key words], (ip2_id, ip2): [ip2's key words], ...}
    """


class TfIdf:
    def __init__(self):
        self.num_docs = 0
        self.vocab = {}

    def add_corpus(self, corpus):
        self._merge_corpus(corpus)

        tfidf_list = []
        for sentence in corpus:
            tfidf_list.append(self.get_tfidf(sentence))
        return tfidf_list

    def _merge_corpus(self, corpus):
        """
        统计语料库，输出词表，并统计包含每个词的文档数。
        """
        self.num_docs = len(corpus)
        for sentence in corpus:
            words = sentence.strip().split()
            words = set(words)
            for word in words:
                self.vocab[word] = self.vocab.get(word, 0.0) + 1.0

    def _get_idf(self, term):
        """
        计算 IDF 值
        """
        return math.log(self.num_docs / (self.vocab.get(term, 0.0) + 1.0))

    def get_tfidf(self, sentence):
        tfidf = {}
        terms = sentence.strip().split()
        terms_set = set(terms)
        num_terms = len(terms)
        for term in terms_set:
            # 计算 TF 值
            tf = float(terms.count(term)) / num_terms
            # 计算 IDF 值，在实际实现时，可以提前将所有词的 IDF 提前计算好，然后直接使用。
            idf = self._get_idf(term)
            # 计算 TF-IDF 值
            tfidf[term] = tf * idf
        return tfidf


corpus_ = [
    "What is the weather like today",
    "what is for dinner tonight",
    "this is question worth pondering",
    "it is a beautiful day today",
    " ",
    "",
    "it is a beautiful day Today today today today today today today today SX-XA-IDC-DNS-RECUR-4.163"
]

corpus_id_ip_ = [
    (1, "123"),
    (2, "123"),
    (3, "123"),
    (6, "123"),
    (10, "123"),
    (23, "123"),
    (39, "123"),
]


def tfidf_calc(corpus, corpus_id_ip):

    tfidf = TfIdf()
    tfidf_values = tfidf.add_corpus(corpus)
    # for tfidf_value in tfidf_values:
    #     print(tfidf_value)
    #     print(sorted(tfidf_value.values(), reverse=True))
    #
    # print(tfidf_values)

    str_list = {}
    for index in range(len(tfidf_values)):
        ip_id_tmp, ip_tmp = corpus_id_ip[index][0], corpus_id_ip[index][1]
        str_list[(ip_id_tmp, ip_tmp)] = {}
        for word, value in tfidf_values[index].items():
            if value not in str_list[(ip_id_tmp, ip_tmp)]:
                str_list[(ip_id_tmp, ip_tmp)][value] = [word]
            else:
                str_list[(ip_id_tmp, ip_tmp)][value].append(word)

    result_list = {}
    for (ip_id, ip) in str_list:
        ip_key_list = []
        sort_words = sorted(str_list[(ip_id, ip)].items(), reverse=True)
        # [(0.7219900393862153, ['account']), (0.28633233321488805, ['draytek', 'vendor', 'vigor', 'hostname', 'pptp']), (0.26229631679778237, ['firmware'])]
        for value, list_tmp in sort_words:
            ip_key_list += list_tmp
            if len(ip_key_list) >= 3:
                break
        result_list[(ip_id, ip)] = ip_key_list

    print(result_list)
    return result_list
