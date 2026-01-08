# Users
USER_READ = "user.read"
USER_UPDATE = "user.update"
USER_DELETE = "user.delete"

# Roles
ROLE_READ = "role.read"
ROLE_CREATE = "role.create"
ROLE_UPDATE = "role.update"
ROLE_DELETE = "role.delete"
ROLE_ASSIGN = "role.assign"

# Permissions
PERMISSION_READ = "permission.read"
PERMISSION_CREATE = "permission.create"

# Content (common)
CONTENT_READ = "content.read"
CONTENT_CREATE = "content.create"
CONTENT_UPDATE = "content.update"
CONTENT_DELETE = "content.delete"

# Books
BOOK_READ = "book.read"
BOOK_CREATE = "book.create"
BOOK_UPDATE = "book.update"
BOOK_DELETE = "book.delete"

# Courses
COURSE_READ = "course.read"
COURSE_CREATE = "course.create"
COURSE_UPDATE = "course.update"
COURSE_DELETE = "course.delete"

# Videos
VIDEO_READ = "video.read"
VIDEO_CREATE = "video.create"
VIDEO_UPDATE = "video.update"
VIDEO_DELETE = "video.delete"

DEV = 'admin.access'


ROLE_PERMISSIONS = {
    "admin": [
        USER_READ, USER_UPDATE, USER_DELETE,
        ROLE_READ, ROLE_CREATE, ROLE_UPDATE, ROLE_DELETE, ROLE_ASSIGN,
        PERMISSION_READ, PERMISSION_CREATE,
        CONTENT_READ, CONTENT_CREATE, CONTENT_UPDATE, CONTENT_DELETE,
        BOOK_READ, BOOK_CREATE, BOOK_UPDATE, BOOK_DELETE,
        COURSE_READ, COURSE_CREATE, COURSE_UPDATE, COURSE_DELETE,
        VIDEO_READ, VIDEO_CREATE, VIDEO_UPDATE, VIDEO_DELETE,DEV
    ],
    "student": [
        CONTENT_READ,
        BOOK_READ,
        COURSE_READ,
        VIDEO_READ,
    ],
    "teacher": [
        CONTENT_READ,
        CONTENT_CREATE,
        CONTENT_UPDATE,
        COURSE_CREATE,
        COURSE_UPDATE,
        VIDEO_CREATE,
        VIDEO_UPDATE,
    ],
    "moderator": [
        CONTENT_READ,
        CONTENT_UPDATE,
        CONTENT_DELETE,
        BOOK_READ,
        BOOK_UPDATE,
        BOOK_DELETE,
        VIDEO_READ,
        VIDEO_UPDATE,
        VIDEO_DELETE,
    ],
}