from ntpath import isabs
from wsgiref.validate import assert_


import pytest


from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

# тесты метода add_new_book

    @pytest.mark.parametrize('name',
        ['Я',
        'Здесь название книги длиной 40 символов.',
        'Корректное название']
    )
    def test_add_new_book_correct_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.books_genre

    @pytest.mark.parametrize('name',
        ['',
        'Слишком длинное название книги - более 40 символов']
    )
    def test_add_new_book_name_not_correct(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.books_genre


    def test_add_new_book_one_book_cant_be_added_twice(self):
        collector = BooksCollector()
        collector.add_new_book('Мастер и Маргарита')
        collector.add_new_book('Мастер и Маргарита')
        assert len(collector.books_genre) == 1


# тесты метода set_book_genre
    @pytest.mark.parametrize('name, genre, expected_genre', [
        ('Книга1', 'Фантастика', 'Фантастика'),
        ('Книга2', 'Ужасы', 'Ужасы')
        ]
    )
    def test_set_book_genre_success(self, name, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == expected_genre

    @pytest.mark.parametrize('name, genre',[
        ('Книга1', 'Жанр не из списка'),
        ('Книга2', None)]
    )
    def test_set_book_genre_failure(self, name, genre):
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == ''

# тест метода get_book_genre
    def test_get_book_genre_name_in_books_genre_book_genre_get(self):
        collector = BooksCollector()
        collector.add_new_book('Властелин колец')
        collector.set_book_genre('Властелин колец', 'Фантастика')
        assert collector.get_book_genre('Властелин колец') == 'Фантастика'


# тест метода get_books_with_specific_genre
    @pytest.mark.parametrize('genre, expected_books', [
        ('Мультфильмы', ['Аленький цветочек', 'Три богатыря']),
        ('Ужасы', ['Оно'])
        ]
    )
    def test_get_books_with_specific_genre_get_list(self, genre, expected_books):
        collector = BooksCollector()
        collector.add_new_book('Аленький цветочек')
        collector.set_book_genre('Аленький цветочек', 'Мультфильмы')
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.add_new_book('Три богатыря')
        collector.set_book_genre('Три богатыря', 'Мультфильмы')
        assert collector.get_books_with_specific_genre(genre) == expected_books


# тест метода get_books_genre
    def test_get_books_genre_invalid_name_book_not_add_in_dictionary(self):
        collector = BooksCollector()
        collector.add_new_book('Мастер и маргарита')
        collector.add_new_book('Приключения Тома Сойера и Гекльберри Финна')  # в названии более 40 символов
        assert collector.books_genre == {'Мастер и маргарита': ''}


# тест метода get_books_for_children
    def test_get_books_for_children_valid_genre_get_list_of_books(self):
        collector = BooksCollector()
        collector.add_new_book('Репка')
        collector.set_book_genre('Репка', 'Мультфильмы')
        collector.add_new_book('Золушка')
        collector.set_book_genre('Золушка', 'Мультфильмы')
        collector.add_new_book('Дракула')
        collector.set_book_genre('Дракула', 'Ужасы')
        collector.genre_age_rating = ['Ужасы']
        assert collector.get_books_for_children() == ['Репка', 'Золушка']


# тесты метода add_book_in_favorites
    @pytest.mark.parametrize('name', [
        ('Алиса в стране чудес'),
        ('12 стульев')
        ]
    )
    def test_add_book_in_favorites_book_from_list(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        assert name in collector.favorites

    @pytest.mark.parametrize('name', [
        ('Книга не из списка')
        ]
    )
    def test_add_book_in_favorites_book_not_in_list(self, name):
        collector = BooksCollector()
        collector.add_book_in_favorites(name)
        assert name not in collector.favorites


# тест метода delete_book_from_favorites
    def test_delete_book_from_favorites_correct_name_of_book_in_favorites_delete_book(self):
        collector = BooksCollector()
        name = 'Остров приключений'
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        collector.delete_book_from_favorites(name)
        assert name not in collector.favorites


# тест метода get_list_of_favorites_books
    def test_get_list_of_favorites_books_name_in_books_genre_get_list(self):
        collector = BooksCollector()
        name = 'Остров приключений'
        collector.add_new_book(name)
        collector.add_book_in_favorites(name)
        assert len(collector.favorites) == 1
