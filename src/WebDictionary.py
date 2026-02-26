import requests
from bs4 import BeautifulSoup

def start():

    WORDLIST = []
    print("Loading...")

    letter = "a"
    for x in range(26):

        site = 1
        Wordlist = []
        while site != 0:

            URL = "https://www.dictionary.com/list/" + letter + "/" + str(site)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = str(soup.find("ul", class_="css-1y59cbu e1j8zk4s0"))

            if results == "None":
                site = 0

            else:

                words = results.replace('<li><a class="css-1c7x6hk-Anchor e3scdxh0" href="https://www.dictionary.com/browse/', '_')
                words = words.replace("</a></li>", "")
                words = words.replace('<ul class="css-1y59cbu e1j8zk4s0">', '')
                words = words.replace("</a><span> | </span>", "")
                words = words.replace('<a class="css-1c7x6hk-Anchor e3scdxh0" href="https://www.thesaurus.com/browse/', '_')
                words = words.replace("</ul>", "")
                words = words.replace('">', "_")

                #Creating a list
                word = ""
                W = []
                for i in range(1, len(words)):

                    if words[i]!="_":
                        word = word + words[i]
                    else:
                        W = W + [word]
                        word = ""

                #Removing expressions etc.
                Wa = []
                chars = "abcdefghijklmnopqrstuvwxyz"
                f = 0
                for i in W:

                    for j in i:
                        if j not in chars:
                            f = 1

                    if f == 0:
                        Wa = Wa + [i]

                    f = 0

                W = Wa

                #Removing doubles
                Wb = []
                for i in W:

                    if i not in Wb:
                        Wb = Wb + [i]

                W = Wb

                site = site + 1

            Wordlist = Wordlist + W

        print(letter)
        letter = chr(ord(letter) + 1)
            
        WORDLIST = WORDLIST + Wordlist

    print("Complete")

    return WORDLIST

def main():

    f = open("WebDic.txt", "w")
    
    WORDLIST = start()
    for i in WORDLIST:
        f.write(i + " ")

    f.close()

main()
