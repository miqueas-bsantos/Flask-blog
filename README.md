# Flask Heroku Blog
This repo contains some sample code to deploy a simple (but complete) Flask application to make a CRUD  simulating a blog. The deployed app counts with the following features:

* Running Python 3.6 🐍
* Access to a SQLAlchemy Database
* Static Image Files and returns dates in TimeStamp

## Steps to access the endpoints of the blog

##### 1. create you user at http://flask-blog-post.herokuapp.com/register

##### 2. Login to http://flask-blog-post.herokuapp.com/login

##### 3. You can use the methods bellow to Test the Application and see the result at http://flask-blog-post.herokuapp.com/home

##### Post a content
```bash
   http://flask-blog-post.herokuapp.com/posts/create
   
   expected body
    {
		"title" : "Miqueas ASDASD",
		"content": "miqueas@teste.com RETSADASD"
    }

    response: 
    {
        "message": "Your Post has been created post.id"
    }
```

##### Update a content
```bash
   http://flask-blog-post.herokuapp.com/posts/update/:id
   
    expected body
    {
		"title" : "Miqueas ASDASD",
		"content": "miqueas@teste.com RETSADASD"
    }

    response: 
    {
        "message": "Your Post has been update post.id"
    }
```

##### GET Posts content
```bash
   http://flask-blog-post.herokuapp.com/posts
   
    expected body:
    {
        "user": 'your@email.com',
		"title" : "Miqueas ASDASD",
		"content": "miqueas@teste.com RETSADASD"
    }
    response:
    [
        {
            "title": "Post 1 ",
            "date_posted": 1557705547.636143
        },
        {
            "title": "Post 2",
            "date_posted": 1558295114.292482
        },
        {
            "title": "Post 3",
            "date_posted": 1558295121.926116
        }
    ]
```

##### GET Post by ID
```bash
   http://flask-blog-post.herokuapp.com/posts/:id
   
    response:
    {
        "title": "talita 1 ", 
        "date_posted": 1557705547.636143
    }
```

##### DELETE Post
```bash
   http://flask-blog-post.herokuapp.com/posts/delete/:id

    response:
    {
        "message": "Your Post has been deleted 15"
    }
```

# Create the virtualenv
$ mkvirtualenv flask-heroku-blog
# Install dependencies
$ pip install -r requirements.txt
# Run the app
$ python run.py
# Now point your browser to localhost:5000
```
