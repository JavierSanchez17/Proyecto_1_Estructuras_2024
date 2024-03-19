import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
from circular_list import CircularList

# Recursos para la conexión con la API de Marvel
publickey = '130c7354b5734b793a253f9087d61518'
hashed = 'a165aa46a0c484d5a49298745951c610'
url = 'http://gateway.marvel.com/v1/public/'
offset_comics = 0  # Nos servira para ver la página de comics en la que se encuentra la API
offset_characters = 0  # Nos servira para ver la página de personajes en la que se encuentra la API
names_comics = CircularList()  # Llamado para los nombres de los comics
names_characters = CircularList()  # Llamado para los nombres de los personajes


def get_comics(page):
    params = {
        'apikey': publickey,
        'ts': 1,
        'hash': hashed,
        'offset': page
    }

    # Obtenemos los datos de los comics agregando la url /comics y los parametros arriba extraidos
    data = requests.get(url + 'comics', params=params).json()
    # Retornamos los datos dentro de las llaves
    return data['data']['results']


def get_characters(page):
    params = {
        'apikey': publickey,
        'ts': 1,
        'hash': hashed,
        'offset': page
    }

    # Obtenemos los datos de los personajes agregando la url /characters y los parametros arriba extraidos
    data = requests.get(url + 'characters', params=params).json()
    # Retornamos los datos dentro de las llaves
    return data['data']['results']


def details_comic(comic):
    # Ventana para los detalles de comics
    details_window = tk.Toplevel()
    details_window.title('Detalles')

    # Marco para los detalles
    details_frame = tk.Frame(details_window)
    details_frame.pack(padx=10, pady=10)

    # Obtener datos para los detalles
    titulo = comic.get('title', 'No disponible')
    isbn = comic.get('isbn', 'No disponible')
    descripcion = comic.get('description', 'No disponible')
    personajes = ', '.join(character['name'] for character in comic.get('characters', {}).get('items', []))
    creadores = ', '.join(creator['name'] for creator in comic.get('creators', {}).get('items', []))
    imagen_url = comic['thumbnail']['path'] + '/portrait_incredible.' + comic['thumbnail']['extension']

    # Intentamos mostrar la imagen del comic con un try except
    try:
        response = requests.get(imagen_url)
        response.raise_for_status()  # Excepcion por solicitud
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((150, 220), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        # Mostrar la imagen del comic
        label_image = ttk.Label(details_frame, image=image)
        label_image.image = image
        label_image.pack(padx=10, pady=10)

    except requests.exceptions.RequestException as e:
        label_image = ttk.Label(details_frame, text=f'Image not Found: {e}')
        label_image.pack(padx=10, pady=10)

    # Mostrar titulo de comic
    title_label = ttk.Label(details_frame, text=f'Titulo: {titulo}')
    title_label.pack(anchor='w', padx=5, pady=5)

    # Mostrar ISBN
    isbn_label = ttk.Label(details_frame, text=f'ISBN: {isbn}')
    isbn_label.pack(anchor='w', padx=5, pady=5)

    # Mostrar descripción del comic
    descripcion_label = ttk.Label(details_frame, text=f'Descripcion: {descripcion}')
    descripcion_label.pack(anchor='w', padx=5, pady=5)

    # Mostrar el nombre e imagen del comic
    characters_label = ttk.Label(details_frame, text=f'Personajes en el comic: {personajes}')
    characters_label.pack(anchor='w', padx=5, pady=5)

    # Mostrar creadores del comic
    creators_label = ttk.Label(details_frame, text=f'Creadores: {creadores}')
    creators_label.pack(anchor='w', padx=5, pady=5)

    # Botón para cerrar la ventana
    close_button = ttk.Button(details_frame, text='Cerrar', command=details_window.destroy)
    close_button.pack(padx=10, pady=10)

    details_window.mainloop()


def details_characters(character):
    # Ventana detalle personajes
    details_window = tk.Toplevel()
    details_window.title('Detalles')

    # Marco para detalles de personaje
    details_frame = ttk.Frame(details_window)
    details_frame.pack(padx=10, pady=10)

    # Obtener detalles del personaje
    nombre = character.get('name', 'No disponible')
    descripcion = character.get('description', 'No disponible')
    image_url = character['thumbnail']['path'] + '/standard_fantastic.' + character['thumbnail']['extension']
    creators = ', '.join(creator['name'] for creator in character.get('creators', {}).get('items', []))
    comics = [comic.get('name', 'No disponible') for comic in character.get('comics', {}).get('items', [])]
    events = [event.get('name', 'No disponible') for event in character.get('events', {}).get('items', [])]

    # Mostrar nombre de los personajes
    name_label = tk.Label(details_frame, text=f'Nombre: {nombre}')
    name_label.pack(anchor='w', padx=5, pady=5)

    # Mostar la imagen del personaje
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((200, 200), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        # Mostrar Imagen
        image_label = ttk.Label(details_frame, image=image)
        image_label.image = image
        image_label.pack(padx=5, pady=5)

    except requests.exceptions.RequestException as e:
        image_label = ttk.Label(details_frame, text=f'Image not found: {e}')
        image_label.pack(padx=5, pady=5)

    # Mostrar la descripcion del personaje
    description_label = tk.Label(details_frame, text=f'Descripcion: {descripcion}')
    description_label.pack(anchor='w', padx=5, pady=5)

    # Mostrar creadores del personaje
    creators_label = tk.Label(details_frame, text=f'Creadores: {creators}')
    creators_label.pack(anchor='w', padx=5, pady=5)

    # Mostrar los comics del personaje
    comics_label = tk.Label(details_frame, text='Comics del personaje')
    comics_label.pack(anchor='w', padx=5, pady=5)

    for i in range(0, len(comics), 10):
        comics_character = comics[i:i + 10]  # Comics desde la pos 0 hasta el 9 o 1-10
        comics_character_text = ', '.join(comics_character)
        comics_character_label = tk.Label(details_frame, text=comics_character_text)
        comics_character_label.pack(anchor='w', padx=5, pady=5)

    # Mostrar los eventos del personaje
    for i in range(0, len(events), 10):
        event_character = events[i:i + 10]
        event_character_text = ', '.join(event_character)
        event_character_label = tk.Label(details_frame, text=event_character_text)
        event_character_label.pack(anchor='w', padx=5, pady=5)

    # Cerrar detalles
    close_button = tk.Button(details_frame, text='Cerrar', command=details_window.destroy)
    close_button.pack(padx=5, pady=5)

    details_window.mainloop()


def page_comics():
    global offset_comics  # Llamamos a la variable global offset_comics
    current_page = 0

    def show_page(page):
        nonlocal current_page  # Llamamos a la variable local current_page
        current_page = page
        comics = get_comics(offset_comics)
        start = current_page * 10
        end = min(start + 10, len(comics))
        for widget in comics_frame.winfo_children():  # Eliminamos algún widget que quede para que no genere conflicto
            widget.destroy()

        for i, comic in enumerate(comics[start:end]):
            nombre = comic.get('title', 'No disponible')
            names_comics.insert_element(nombre)
            image_url = comic['thumbnail']['path'] + '/portrait_incredible.' + comic['thumbnail']['extension']

            try:
                response = requests.get(image_url)
                response.raise_for_status()
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((150, 220), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)

                label_comic_image = tk.Label(comics_frame, image=image)
                label_comic_image.image = image
                label_comic_image.grid(row=(i // 5) * 3, column=(i % 5), padx=5, pady=5)

            except requests.exceptions.RequestException as e:
                label_comic_image = tk.Label(comics_frame, text=f'Image not found: {e}')
                label_comic_image.grid(row=(i // 5) * 3, column=(i % 5), padx=5, pady=5)

            # Mostrar boton de detalles
            details_button = tk.Button(comics_frame, text='Detalles', command=lambda com=comic: details_comic(com))
            details_button.grid(row=(i // 5) * 3 + 2, column=(i % 5), padx=5, pady=5)

        list_names = names_comics.get_list()
        for i in range(len(list_names)):
            # Mostar, nombre del comic debajo de la imagen
            name_label = tk.Label(comics_frame, text=list_names[i])
            name_label.grid(row=(i // 5) * 3 + 1, column=(i % 5), padx=5, pady=5)

    def pag_anterior():
        global offset_comics
        nonlocal current_page
        names_comics.delete_all()
        if offset_comics > 0:
            if current_page > 0:
                current_page -= 1
            elif current_page == 0:
                offset_comics -= 1
                current_page = 1
            show_page(current_page)
        elif offset_comics == 0:
            if current_page > 0:
                current_page -= 1
                show_page(current_page)

    def pag_siguiente():
        global offset_comics
        nonlocal current_page
        names_comics.delete_all()
        current_page += 1
        if current_page == 2:
            offset_comics += 1
            current_page = 0
        show_page(current_page)

    comics_window = tk.Toplevel()
    comics_window.title('Comics')

    comics_frame = ttk.Frame(comics_window)
    comics_frame.pack(padx=10, pady=10)

    current_offset = 0

    show_page(current_offset)

    navegator_frame = ttk.Frame(comics_window)
    navegator_frame.pack(pady=5)

    prev_button = ttk.Button(navegator_frame, text='Página Anterior', command=pag_anterior)
    prev_button.grid(row=0, column=0, padx=5)

    next_button = ttk.Button(navegator_frame, text='Página Siguiente', command=pag_siguiente)
    next_button.grid(row=0, column=2, padx=5)

    home_button = ttk.Button(navegator_frame, text='Regresar a la Página Principal', command=comics_window.destroy)
    home_button.grid(row=0, column=1, padx=5)


def page_characters():
    global offset_characters  # Llamamos a la variable global offset_characters
    current_page = 0

    def show_page(page):
        nonlocal current_page  # Llamamos a la variable local current_page
        current_page = page
        characters = get_characters(offset_characters)
        start = current_page * 10
        end = min(start + 10, len(characters))
        for widget in characters_frame.winfo_children():  # Eliminamos widget para evitar conflictos
            widget.destroy()

        for i, character in enumerate(characters[start:end]):
            nombre = character.get('name', 'No disponible')
            names_characters.insert_element(nombre)
            image_url = character['thumbnail']['path'] + '/portrait_incredible.' + character['thumbnail']['extension']

            try:
                response = requests.get(image_url)
                response.raise_for_status()
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((150, 220), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)

                label_character_image = tk.Label(characters_frame, image=image)
                label_character_image.image = image
                label_character_image.grid(row=(i // 5) * 3, column=(i % 5), padx=5, pady=5)

            except requests.exceptions.RequestException as e:
                label_character_image = tk.Label(characters_frame, text=f'Image not found: {e}')
                label_character_image.grid(row=(i // 5) * 3, column=(i % 5), padx=5, pady=5)

            # Mostrar boton de detalles
            details_button = tk.Button(characters_frame, text='Detalles', command=lambda char=character:
                                       details_comic(char))
            details_button.grid(row=(i // 5) * 3 + 2, column=(i % 5), padx=5, pady=5)

        list_names = names_characters.get_list()
        for i in range(len(list_names)):
            # Mostar, nombre del personaje debajo de la imagen
            name_label = tk.Label(characters_frame, text=list_names[i])
            name_label.grid(row=(i // 5) * 3 + 1, column=(i % 5), padx=5, pady=5)

    def pag_anterior():
        global offset_characters
        nonlocal current_page
        names_characters.delete_all()
        if offset_characters > 0:
            if current_page > 0:
                current_page -= 1
            elif current_page == 0:
                offset_characters -= 1
                current_page = 1
            show_page(current_page)
        elif offset_characters == 0:
            if current_page > 0:
                current_page -= 1
                show_page(current_page)

    def pag_siguiente():
        global offset_characters
        nonlocal current_page
        names_characters.delete_all()
        current_page += 1
        if current_page == 2:
            offset_characters += 1
            current_page = 0
        show_page(current_page)

    characters_window = tk.Toplevel()
    characters_window.title('Personajes')

    characters_frame = ttk.Frame(characters_window)
    characters_frame.pack(padx=10, pady=10)

    current_offset = 0

    show_page(current_offset)

    navegator_frame = ttk.Frame(characters_window)
    navegator_frame.pack(pady=5)

    prev_button = ttk.Button(navegator_frame, text='Página Anterior', command=pag_anterior)
    prev_button.grid(row=0, column=0, padx=5)

    next_button = ttk.Button(navegator_frame, text='Página Siguiente', command=pag_siguiente)
    next_button.grid(row=0, column=2, padx=5)

    home_button = ttk.Button(navegator_frame, text='Regresar a la Página Principal', command=characters_window.destroy)
    home_button.grid(row=0, column=1, padx=5)


def page_creators():
    creator_window = tk.Toplevel()
    creator_window.configure(bg='black')
    creator_window.title('Creadores del Código')

    creator_frame = tk.Frame(creator_window)
    creator_frame.configure(bg='black')
    creator_frame.pack(padx=10, pady=10)

    # Información de los creadores
    # Nombre del creador
    name_label = tk.Label(creator_frame, text='Creador: Francisco Javier Sánchez Tasej', fg='white', bg='black',
                          font=('Arial Black', 15))
    name_label.pack(padx=5, pady=5)

    # Imagen del creador
    image_creator_path = ('C:/Users/INTEL i7/Documents/URL 1er Ciclo 2024/Estructura de Datos '
                          'l/Proyecto 1 - Estructura de Datos l/Images/Profile_Photo.png')
    image_creator = Image.open(image_creator_path)
    image_creator = image_creator.resize((200, 200), Image.LANCZOS)
    creator_photo = ImageTk.PhotoImage(image_creator)

    label_creator_image = tk.Label(creator_frame, image=creator_photo, bg='red')
    label_creator_image.photo = creator_photo
    label_creator_image.pack(padx=5, pady=5)

    label_carnet = tk.Label(creator_frame, text='Carnet: 2012421', fg='white', bg='black', font=('Arial Black', 15))
    label_carnet.pack(padx=5, pady=5)
    # Boton para regresar al menu principal
    return_button = tk.Button(creator_frame, text='Regresar al menu principal', fg='white', bg='black',
                              font=('Arial Black', 15), command=creator_window.destroy, borderwidth=0)
    return_button.bind('<Enter>', lambda event: return_button.config(bg='#DDDDDD'))
    return_button.bind('<Leave>', lambda event: return_button.config(bg='black'))
    return_button.pack(padx=5, pady=10)

    creator_window.mainloop()


def main():
    master = tk.Tk()
    master.title('API Marvel')
    master.configure(bg='black')

    main_frame = tk.Frame(master)
    main_frame.configure(bg='black')
    main_frame.pack(padx=10, pady=10)

    marvel_image_path = ('C:/Users/INTEL i7/Documents/URL 1er Ciclo 2024/Estructura de Datos '
                         'l/Proyecto 1 - Estructura de Datos l/Images/logo_marvel.png')
    marvel_image = Image.open(marvel_image_path)
    marvel_image = marvel_image.resize((600, 300), Image.LANCZOS)
    photo_marvel = ImageTk.PhotoImage(marvel_image)

    label_image = ttk.Label(main_frame, image=photo_marvel, background='black')
    label_image.marvel_image = photo_marvel
    label_image.grid(row=0, column=0, padx=5, pady=5)

    # Boton para entrar a la pagina de comics
    comics_button = tk.Button(main_frame, text='CÓMICS', width=40, bg='black', fg='white', font=('Arial Black', 15),
                              command=lambda: page_comics(), borderwidth=0)
    comics_button.bind('<Enter>', lambda event: comics_button.config(bg='#DDDDDD'))
    comics_button.bind('<Leave>', lambda event: comics_button.config(bg='black'))
    comics_button.grid(row=1, column=0, padx=5, pady=5)

    # Boton para entrar a la página de personajes
    character_button = tk.Button(main_frame, text='PERSONAJES', width=40, bg='black', fg='white',
                                 font=('Arial Black', 15), command=lambda: page_characters(), borderwidth=0)
    character_button.bind('<Enter>', lambda event: character_button.config(bg='#DDDDDD'))
    character_button.bind('<Leave>', lambda event: character_button.config(bg='black'))
    character_button.grid(row=2, column=0, padx=5, pady=5)

    # Boton para entrar a la página del creador
    creator_button = tk.Button(main_frame, text='CREADOR', width=40, bg='black', fg='white', font=('Arial Black', 15),
                               command=lambda: page_creators(), borderwidth=0)
    creator_button.bind('<Enter>', lambda event: creator_button.config(bg='#DDDDDD'))
    creator_button.bind('<Leave>', lambda event: creator_button.config(bg='black'))
    creator_button.grid(row=3, column=0, padx=5, pady=5)

    # Boton para salir
    exit_button = tk.Button(main_frame, text='SALIR', width=40, bg='black', fg='white', font=('Arial Black', 15),
                            command=master.destroy, borderwidth=0)
    exit_button.bind('<Enter>', lambda event: exit_button.config(bg='#DDDDDD'))
    exit_button.bind('<Leave>', lambda event: exit_button.config(bg='black'))
    exit_button.grid(row=4, column=0, padx=5, pady=5)

    master.mainloop()


if __name__ == '__main__':
    main()
