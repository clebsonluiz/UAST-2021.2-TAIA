import csv
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


class TwitterListener(StreamListener):

    def __init__(self, file: str , track_list: list):
        assert file is not None and track_list is not None
        assert len(file) > 0 and len(track_list) > 0
        self.cont_tweet = 0
        self.max_tweets = 100000000000000000000
        self.track_list = track_list
        self.file_name = file + "" if ".csv" in file else ".csv"

    def on_data(self, data):
        # incrementa o contador de tweets
        self.cont_tweet = self.cont_tweet + 1
        try:

            as_key_str: bool = False

            tweet = json.loads(data)
            
            body_content: str = tweet.get('extended_tweet')['full_text'] \
                if 'extended_tweet' in tweet else tweet.get('text')


            for key_str in self.track_list:
                if key_str in body_content:
                    as_key_str = True
                    break

            if "RT " not in tweet.get('text') and as_key_str \
                and "pt" in tweet.get('lang'):
                
                print(tweet)

                meu_arquivo = open(self.file_name, mode='a', newline='')
                writer = csv.writer(meu_arquivo, delimiter=';', quotechar=';')

                writer.writerow([tweet.get('created_at'), '[' + tweet.get('id_str') + ']',
                                body_content.replace("\n", " ")])
                meu_arquivo.close()

        except BaseException as erro:
            print('Erro: ' + str(erro))
        # condição de parada
        if self.cont_tweet >= self.max_tweets:
            # retorne false
            return False

    def on_error(self, status):
        # escreve na tela o status do erro
        print
        str(status)

    

def main():
    # Complete aqui com o valor da "access_token" gerada para você
    access_token = ""
    # Complete aqui com o valor da "access_token_secret" gerada para você
    access_token_secret = ""
    # Complete aqui com o valor da "consumer_key" gerada para você (API Key)
    consumer_key = ""
    # Complete aqui com o valor da "consumer_secret" gerada para você (API Secret Key)
    consumer_secret = ""

    # Track list para filtrar os assuntos
    track_list: list[str] = ["adultoney","neymar", "Neymar"]
    # Nome do arquivo onde será salvo
    file_name: str = "ney_base.csv"

    tl = TwitterListener(file_name, track_list)
    oauth = OAuthHandler(consumer_key, consumer_secret)
    oauth.set_access_token(access_token, access_token_secret)

    stream = Stream(oauth, tl)
    stream.filter(track=track_list)


if __name__ == "__main__":
    main()