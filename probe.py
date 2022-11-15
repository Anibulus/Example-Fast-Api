import urllib.parse as parse
import requests 

def run():

    MAIN_API = 'http://api.themoviedb.org/3/search/movie?'
    KEY = 'dd0ab6662daffeeddd18ebbe18f9f872'
    nombre_pelicula = input('Ingrese el nombre de la película: ')

    url = MAIN_API + parse.urlencode({'api_key' : KEY, 'query' : nombre_pelicula})
    #print(url)

    json_data = requests.get(url).json()
    #print(json_data)

    str_titulo = json_data['results'][0]['title']
    str_fecha = json_data['results'][0]['release_date']
    str_voto = json_data['results'][0]['vote_average']

    numero = 1
    while numero >= 10:
        numero += 1

    print("\n\nResultados de peliculas")
    resultados = requests.get(url).json()
    for result in resultados["results"]:
        print([numero], result["original_title"])
        numero += 1
        args = {'api_key':KEY, 'query':nombre_pelicula}
    response = requests.get(MAIN_API, params=args)

    if response.status_code == 200:
        response_json = response.json()

    peliculas = response_json["results"]

    print("\n\nListado de peliculas")
    for index, pelicula in enumerate(peliculas, 1):
        print(f"[{index}] {pelicula['title']}")

    indice_peli = int(input('\nseleccionar pelicula: '))

    for k, v in peliculas[indice_peli - 1].items():

        print(f"'{k}' : {v}")

    
    Genre_api = 'https://api.themoviedb.org/3/genre/movie/list?'
    KEY = 'dd0ab6662daffeeddd18ebbe18f9f872'
    url = Genre_api + parse.urlencode({'api_key' : KEY, 'query' : ""})
    json_data = requests.get(url).json()
    generos = {genero['name']: genero['id'] for genero in json_data['genres']}

    for nombre, gid in generos.items():
        print(f"[{nombre.center(17):<17}] | ID: {gid}")

    genero = input("Genero: ")
    if genero[0].upper() +genero[1:].lower() in list(generos.keys()):
        print("valido")
        genero_id = generos.get(genero[0].upper() +genero[1:].lower())
        movies = list(filter(lambda x : genero_id in x.get('genre_ids', 0), peliculas))
        print(movies)
    else:
        print("no valido")
    



if __name__ == '__main__':
    run()
