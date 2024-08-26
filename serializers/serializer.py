def convertBlog(blog)->dict:
    return{
        'username':str(blog['username']),
        'email':str(blog['email']),
        'id':str(blog['_id']),
        'title':blog['title'],
        'description':blog['description'],
        'author':blog['author']
    }
    
def convertBlogs(blogs)->list:
    return [convertBlog(blog) for blog in blogs]