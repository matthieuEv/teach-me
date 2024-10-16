# Teach Me

Running on `python@3.12.7`

```
(Prompt) -> Script -> text-to-speetch -> audio-to-face
                   -> text-to-image
````

# Initial Prompt

You are a teacher. Teach me about (...). You will make separated chapters, and return a response like this json. (...), there is a max of 3 chapters. In the end, you will have to make a QCM base on the json format. There is a max of 5 questions.

## Script Json Format

```json
{
    "script": {
        "title_course": str,
        "chapters": [
            {
                "title_chapter": str,
                "content": str
            },
            ...
        ]
    },
    "qcm": [
        {
            "question": str,
            "list_answers": [str]
            "index_good_answer": int,
        }
    ]
}
```

## Description format

if needed, you can integrate picture in the content of the chapter by describing what you want in double square brackets.

`exemple: [[a picture of a town in Kansas]]`