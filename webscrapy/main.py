import os
from urllib.parse import urlparse

from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import Comic, Revista
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
session = requests.Session()
box = []


def link_to_image(links):
    if isinstance(links, list):
        for link in links:
            try:
                print(link)
                response = session.get(link, headers=headers, timeout=None)
                soup = BeautifulSoup(response.text, 'lxml')
                texto = soup.select_one('main > article > div > header > h1').get_text()
                imagem = soup.select('dl> dt > img')
                desc = soup.select_one('main > article > div > p').get_text()



                # nome = os.path.basename(imagem[0].get('src'))
                nome = imagem[0].get('src')
                # conteudo = requests.get(imagem[0].get('src'), timeout=None).content
                # pre_image = SimpleUploadedFile(nome, conteudo)
                try:
                    if Comic.objects.get(name=texto):
                        base = Comic.objects.get(name=texto)
                        rvt = Revista.objects.filter(base=base)
                        print(rvt.count())
                        if rvt.count() < len(imagem):
                            print('revista a atualizar')
                        else:
                            print('revista já existe')
                except:
                    print(texto)
                    comic = Comic(name=texto, description=desc, picture=nome)
                    comic.save()
                    for img in imagem:
                        revista_name = os.path.basename(img.get('src'))
                        url_img = img.get('src')
                        # revista_conteudo = requests.get(url_img, headers=headers).content
                        # pre_revista = SimpleUploadedFile(revista_name, revista_conteudo)
                        revista = Revista(base=comic, file=url_img)
                        revista.save()
            except IndexError:
                pass
    else:
        response = session.get(links, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        texto = soup.select_one('main > article > div > header > h1').get_text()
        imagem = soup.select('dl> dt > img')
        desc = soup.select_one('main > article > div > p').get_text()

        print(texto)
        nome = os.path.basename(imagem[0].get('src'))
        conteudo = requests.get(imagem[0].get('src')).content
        pre_image = SimpleUploadedFile(nome, conteudo)
        comic = Comic(name=texto, description=desc, picture=pre_image)
        comic.save()
        for img in imagem:
            revista_name = os.path.basename(img.get('src'))
            url_img = img.get('src')
            revista_conteudo = requests.get(url_img, headers=headers).content
            pre_revista = SimpleUploadedFile(revista_name, revista_conteudo)
            revista = Revista(base=comic, file=pre_revista)
            revista.save()


def web_link(link, seletor='div > figure > a', page='a.next.page-numbers'):
    parse_link = urlparse(link)
    verificador = f'{parse_link.scheme}://{parse_link.netloc}/'
    print(link)
    response = session.get(link, headers=headers, timeout=None)
    soup = BeautifulSoup(response.text, 'lxml')
    urls = soup.select(seletor)
    for url in urls:
        pegarhref = url.get('href')
        if verificador in pegarhref:
            box.append(pegarhref)
        else:
            continue
    try:
        proxima = soup.select_one(page).get('href')
        if proxima:
            recalback(proxima, web_link, seletor, page)
    except AttributeError:
        pass
    session.close()
    link_to_image(list(set(box)))


def recalback(r_url, r_chamada, seletor, page):
    r_chamada(link=r_url, seletor=seletor, page=page)


if __name__ == '__main__':
    web_link('https://www.quadrinhoseroticos.blog/page/200/', 'div > figure > a', 'a.next.page-numbers')
