# User Authentication System 🚀

This is a small project user authentication system project built using Python tech stack.

> [!IMPORTANT]
> Please create a MongoDB database called **UsersDB** and inside it create a collection called **users**. [click here](https://account.mongodb.com/account/login)

## URL Endpoints

#### User Sign up 📌

```bash
# URL: http://127.0.0.1:8080/api/v1/product/signup

# Or you copy past below command on your terminal

>> curl -d "first_name=John" -d "last_name=Doe" -d "username=johndoe88" -d "password=johnspassowrd" -d "email=john@gmail.com" -X 'POST' http://127.0.0.1:8080/api/v1/product/signup
```

#### Log in 📌

```bash
# URL: http://127.0.0.1:8080/api/v1/product/login

>> curl -d "username=johndoe88" -d "password=johnspassowrd" -X 'POST' http://127.0.0.1:8080/api/v1/product/login
```

#### User authorized actions 📌

These actions are updating password only when use is logged in.

```bash
# inprocess
```

# Tech stack 🦖

- FastAPI
- Pydantic
- MongoDB
- JWT

# Goals

![image](./images/goals.png)
