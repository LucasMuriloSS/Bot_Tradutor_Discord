import discord
from discord import app_commands
from googletrans import Translator
from PyDictionary import PyDictionary
import urllib.request
from bs4 import BeautifulSoup
from unidecode import unidecode
import re


translator = Translator()
dictionary = PyDictionary()
intents = discord.Intents.default()
intents.message_content = True


class client(discord.Client):

  def __init__(self):

    super().__init__(intents=intents)

    intents.message_content = True

    self.synced = False  #Impedir que o bot sincronize os comandos mais de uma vez

  async def on_message(self, Message):

    if '>def' in Message.content[:4]:

      palavra = Message.content.split()

      palavra1 = palavra[1]

      palavra2 = unidecode(palavra1)

      palavra2 = palavra2.lower()

      try:
        url = f'https://www.dicio.com.br/{palavra2}'
        response = urllib.request.urlopen(url)
        html_content = response.read()
  
        # Analisando o HTML com BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
  
        # Obtendo o texto do artigo
        paragrafo = soup.find('p', {'class': 'significado textonovo'})
  
        spans = paragrafo.find_all('span')
  
        segundo_spam = spans[1].text
        #print(segundo_spam)
  
        embed = discord.Embed(
            title=f'Definição de {palavra1}',
            description=f'{segundo_spam}',
            color=0x0099ff  # Cor do embed em hexadecimal
        )
  
        await Message.reply(embed=embed)

      except:

        pass

    if '>t' in Message.content[:2]:
      
      palavra = Message.content.split()
      palavra2 = palavra[1]
      texto = f'Quero a tradução de [{palavra2}]' 
      # A palavra foi colocada em uma frase pois por algum motivo a biblioteca não traduz algumas palavras únicas

      try:

        traducao = translator.translate(texto, dest='en')
        padrao = r"\[([^\]]+)\]"
        correspondencias = re.findall(padrao, traducao.text)
        
        if correspondencias:

          embed = discord.Embed(
              title=f'Tradução',
              description=f'{correspondencias[0]}',
              color=0x0099ff  # Cor do embed em hexadecimal
          )
          
          await Message.reply(embed=embed)

      except:

        pass

aclient = client()

aclient.run(
    'TOKEN DO BOT')
