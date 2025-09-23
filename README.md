## Object & Image to Image Generation

### Model Inputs

**Image** - Image of the user

**Object** - The plan activity of the user (eg. Cricket, Movie, Shopping, etc.)

---

### API Endpoints

- ``` GET /health ``` - Check if the server is functioning properly.

- ``` POST /upload ``` - Here user have to give their inputs.

---

### Run Cmd

$ flask run

---

### Postman Query

Body -> form-data

```
Key                    Value

- image                - @attachment

- text                 - object
```