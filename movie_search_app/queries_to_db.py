import mysql.connector
from prettytable import PrettyTable
from movie_search_app.utils import color_text
from colorama import Fore, Style, init

def update_top_queries(search_condition):
    try:
        conn = mysql.connector.connect(
            host='mysql.itcareerhub.de',
            user='ich1',
            password='ich1_password_ilovedbs',
            database='310524ptm_oleksiy'
        )
        cursor = conn.cursor()

        # Проверка, существует ли уже такой запрос
        query = "SELECT cnt FROM top_queries WHERE query = %s"
        cursor.execute(query, (search_condition,))
        result = cursor.fetchone()

        if result:
            # Если запрос уже существует, увеличиваем счетчик на 1
            update_query = "UPDATE top_queries SET cnt = cnt + 1 WHERE query = %s"
            cursor.execute(update_query, (search_condition,))
        else:
            # Если запрос новый, добавляем его с cnt = 1
            insert_query = "INSERT INTO top_queries (query, cnt) VALUES (%s, 1)"
            cursor.execute(insert_query, (search_condition,))

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def show_top_queries():
    try:
        conn = mysql.connector.connect(
            host='mysql.itcareerhub.de',
            user='ich1',
            password='ich1_password_ilovedbs',
            database='310524ptm_oleksiy'
        )
        cursor = conn.cursor()

        query = "SELECT query, cnt FROM top_queries ORDER BY cnt DESC LIMIT 10"
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            table = PrettyTable()

            # Установка цветного текста для заголовков таблицы
            table.field_names = [
                color_text("Query", Fore.YELLOW),
                color_text("Count", Fore.GREEN)
            ]
            for row in results:
                table.add_row([color_text(row[0], Fore.YELLOW), color_text(row[1], Fore.GREEN)])

            print("\nTop 10 Queries:")
            # Окрашиваем рамки таблицы в зеленый цвет
            print(Fore.GREEN + str(table))
        else:
            print("No queries found in the top_queries table.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def search_movies(search_condition, search_type):
    try:
        conn = mysql.connector.connect(
            host='ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
            user='ich1',
            password='password',
            database='sakila'
        )
        cursor = conn.cursor()

        base_query = """
        SELECT 
            film.film_id AS film_id,
            film.title AS title,
            film.release_year,
            category.name AS category,
            film.description AS description,
            film.rental_rate as rating,
            GROUP_CONCAT(CONCAT(actor.first_name, ' ', actor.last_name) SEPARATOR ', ') AS actors,
            film.length AS length
        FROM
            film
            LEFT JOIN film_category ON film_category.film_id = film.film_id
            LEFT JOIN category ON category.category_id = film_category.category_id
            LEFT JOIN film_actor ON film.film_id = film_actor.film_id
            LEFT JOIN actor ON film_actor.actor_id = actor.actor_id
        """

        if search_condition in ['.', ' ', '']:
            query = base_query + "GROUP BY film.film_id, category.name;"
            cursor.execute(query)
        else:
            if search_type == 'title':
                query = base_query + "WHERE film.title LIKE %s "
                parameters = (f'%{search_condition}%',)
            elif search_type == 'release_year':
                query = base_query + "WHERE film.release_year LIKE %s "
                parameters = (f'%{search_condition}%',)
            elif search_type == 'category':
                query = base_query + "WHERE category.name LIKE %s "
                parameters = (f'%{search_condition}%',)
            elif search_type == 'description':
                query = base_query + "WHERE film.description LIKE %s "
                parameters = (f'%{search_condition}%',)
            elif search_type == 'rating':
                if search_condition == '0-1':
                    query = base_query + "WHERE film.rental_rate BETWEEN 0 AND 1 "
                    parameters = ()
                elif search_condition == '1+':
                    query = base_query + "WHERE film.rental_rate > 1 "
                    parameters = ()
                elif search_condition == '2+':
                    query = base_query + "WHERE film.rental_rate > 2 "
                    parameters = ()
                elif search_condition == '3+':
                    query = base_query + "WHERE film.rental_rate > 3 "
                    parameters = ()
                elif search_condition == 'Top':
                    query = base_query + "WHERE film.rental_rate = (SELECT MAX(film.rental_rate) FROM film) "
                    parameters = ()
                else:
                    query = base_query
                    parameters = ()
            elif search_type == 'actors':
                query = base_query + "WHERE CONCAT(actor.first_name, ' ', actor.last_name) LIKE %s "
                parameters = (f'%{search_condition}%',)
            elif search_type == 'length':
                query = base_query + "WHERE film.length LIKE %s "
                parameters = (f'%{search_condition}%',)
            else:
                query = base_query
                parameters = ()

            query += "GROUP BY film.film_id, category.name;"
            cursor.execute(query, parameters)

        results = cursor.fetchall()
        num_results = len(results)

        if num_results == 0:
            print("Nothing found for the given search criteria.")
        else:
            print(f"\nFound {num_results} movies:")
            table = PrettyTable()

            # Установка цветного текста для заголовков таблицы
            table.field_names = [
                color_text("ID", Fore.WHITE),
                color_text("Title", Fore.YELLOW),
                color_text("Release Year", Fore.WHITE),
                color_text("Category", Fore.RED),
                color_text("Description", Fore.LIGHTBLACK_EX),
                color_text("Rating", Fore.WHITE),
                color_text("Actors", Fore.LIGHTWHITE_EX),
                color_text("Length", Fore.WHITE)
            ]

            for row in results:
                colored_row = [
                    color_text(row[0], Fore.WHITE),
                    color_text(row[1], Fore.YELLOW),
                    color_text(row[2], Fore.WHITE),
                    color_text(row[3], Fore.RED),
                    color_text(row[4], Fore.LIGHTBLACK_EX),
                    color_text(row[5], Fore.WHITE),
                    color_text(row[6], Fore.LIGHTWHITE_EX),
                    color_text(row[7], Fore.WHITE)
                ]
                table.add_row(colored_row)

            # Установка выравнивания по левому краю для определенных столбцов
            table.align["Title"] = "l"
            table.align["Description"] = "l"
            table.align["Actors"] = "l"

            # Установка максимальной ширины для каждого столбца
            table.max_width["ID"] = 5
            table.max_width["Title"] = max(len(row[1]) for row in results) if results else 20
            table.max_width["Release Year"] = 12
            table.max_width["Category"] = max(len(row[3]) for row in results) if results else 20
            table.max_width["Description"] = max(len(row[4]) for row in results) if results else 40
            table.max_width["Rating"] = 7
            table.max_width["Actors"] = max(len(row[6]) for row in results) if results else 30
            table.max_width["Length"] = 6

            # Окрашиваем рамки таблицы в зеленый цвет
            print(Fore.GREEN + str(table))

        update_top_queries(search_condition)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()