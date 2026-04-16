### POST /posts
**Request Body:**
{
    "title": "My First Blog Post",
    "content": "This is the content of the post...",
    "author_id": 1,
    "tags": ["python", "backend"]
}

**Success Response - 201**
{
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of the post...",
    "author_id": 1,
    "tags": ["python", "backend"],
    "created_at": "2026-04-13",
    "comment_count": 0
}

**Errors**
Missing Title - 422 - VALIDATION_ERROR
author_id does not exist - 404 - USER_NOT_FOUND
Server Crash - 500 - SERVER_ERROR

### GET /posts/{id}

**id: id of the blog**

Success Response - 200
{
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of the post...",
    "author_id": 1,
    "tags": ["python", "backend"],
    "created_at": "2026-04-13",
    "comment_count": 0
}

**Errors:**
Post not found - 404 - POST_NOT_FOUND
Server crash - 500 - SERVER_ERROR

### PUT /posts/{id}
**id: id of the blog**
{
    "title": "First Blog"
    "content": "Content of the this blog..."
    "tags": ["python"]
}

Success Response - 200
{
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of the post...",
    "author_id": 1,
    "tags": ["python", "backend"],
    "created_at": "2026-04-13",
    "comment_count": 0
}

**Errors:**
Post not found - 404 - POST_NOT_FOUND
Missing required field - VALIDATION_ERROR
Server Crash - 500 - SERVER_ERROR

### DELETE /posts/{id}
**id - id of the blog posted**

Success Response - 200
{
    "message": "Post deleted successfully"
}

**Errors:**
Server crash - 500 - SERVER_ERROR
Post not found - 404 - POST_NOT_FOUND

### GET /posts
**Success Response - 200**
[
    {
        "id": 1,
        "title": "My First Blog Post",
        "content": "This is the content of the post...",
        "author_id": 1,
        "tags": ["python", "backend"],
        "created_at": "2026-04-13",
        "comment_count": 0
    }
]

**Errors:**
Server crash - 500 - SERVER_ERROR

### GET /posts/{id}/comments
Success Response - 200
[
    {
        "id": 11,
        "post_id": 1,
        "author_id": 3,
        "content": "Great post!",
        "created_at": "2026-04-13"
    }
]

**Errors:**
Server crash - 500 - SERVER_ERROR
Post not found - 404 - POST_NOT_FOUND

### POST /posts/{id}/comments
{
    "comment_content": "First comment"
    "author_id": 3
}

Success Response - 201
{
    "comment_id": 11,
    "comment_content": "First comment",
    "created_at": "2026-04-13"
}

**Errors:**
Post not found - 404 - POST_NOT_FOUND
author_id not found - 404 - USER_NOT_FOUND
Empty content - 422 - VALIDATION_ERROR
Server crash - 500 - SERVER_ERROR

### DELETE /posts/{id}/comments/{comment_id}
Success Response - 200
{
    "comment_id": 11,
    "comment_content": "First comment",
    "created_at": "2026-04-13"
}

**Errors:**
Post not found - 404 - POST_NOT_FOUND
Comment not found - 404 - COMMENT_NOT_FOUND
Server crash - 500 - SERVER_ERROR