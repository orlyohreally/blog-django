# Blog
This project is a very simple blog with big functionality:
* for admin and staff
    * creating, editing, deleting posts
    * admin interface
* for all users
    * user authorization
    * commenting blog posts
    * sharing posts on social media (Twitter and Facebook)

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development purposes.

### Requirements
Python 3.5, 3.6

### Installation

Create virtual environment **blog_env**
```
virtualenv blog_env
```

Clone the repository to created folder
```
cd blog_env
git clone https://github.com/orlyohreally/blog-django.git
```

Install all the requirements for the project
```
cd Scripts
pip install -r ..\blog-django\requirements.txt
```

Activate virtual environment by running activate.bat file
```
activate.bat
```

Go to the project and create the database
```
cd ..\blog-django
manage.py migrate
```

Only admin or staff can create new posts so create super user
```
manage.py createsuperuser
```

Run the development server
```
manage.py runserver
```

The project will be available at http://127.0.0.1:8000/posts/. Admin page is at http://127.0.0.1:8000/admin/.

## Built with
* [Django](https://www.djangoproject.com/) - used Python Web framework
* [Bootstrap](http://getbootstrap.com/) - used open source toolkit  to create interface

## Authors
* **Orly Knop** - [orlyohreally](https://github.com/orlyohreally)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details