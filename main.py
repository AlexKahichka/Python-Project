from prettytable import PrettyTable
from colorama import Fore, Style, init

from movie_search_app.queries_to_db import show_top_queries, search_movies

# Инициализация colorama
init(autoreset=True)


def main():
    print("Welcome to the movie search application!")

    while True:
        print("\nChoose an option:")
        print("1. Search for movies")
        print("2. View top 10 search queries")
        print("3. Exit")

        choice = input("Enter the number of your choice: ").strip()

        if choice == '1':
            print("\nChoose a search criterion:")
            print("1. Search by title")
            print("2. Search by release year")
            print("3. Search by category")
            print("4. Search by description")
            print("5. Search by rating")
            print("6. Search by actors")
            print("7. Search by length")

            search_choice = input("Enter the number of the search criterion: ").strip()

            if search_choice == '1':
                search_condition = input("Enter the movie title to search: ")
                search_type = 'title'
            elif search_choice == '2':
                search_condition = input("Enter the release year to search: ")
                search_type = 'release_year'
            elif search_choice == '3':
                search_condition = input("Enter the category to search: ")
                search_type = 'category'
            elif search_choice == '4':
                search_condition = input("Enter the movie description to search: ")
                search_type = 'description'
            elif search_choice == '5':
                print("\nChoose a rating filter:")
                print("1. Rating between 0 and 1")
                print("2. Rating above 1")
                print("3. Rating above 2")
                print("4. Rating above 3")
                print("5. Top rating")

                rating_choice = input("Enter the number of the rating filter: ").strip()

                if rating_choice == '1':
                    search_condition = '0-1'
                elif rating_choice == '2':
                    search_condition = '1+'
                elif rating_choice == '3':
                    search_condition = '2+'
                elif rating_choice == '4':
                    search_condition = '3+'
                elif rating_choice == '5':
                    search_condition = 'Top'
                else:
                    print("Invalid choice. Please select a number between 1 and 5.")
                    continue

                search_type = 'rating'
            elif search_choice == '6':
                search_condition = input("Enter the actor's name to search: ")
                search_type = 'actors'
            elif search_choice == '7':
                search_condition = input("Enter the movie length to search: ")
                search_type = 'length'
            else:
                print("Invalid choice. Please select a number between 1 and 7.")
                continue

            search_movies(search_condition, search_type)

        elif choice == '2':
            show_top_queries()

        elif choice == '3':
            print("Exiting the application...")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
