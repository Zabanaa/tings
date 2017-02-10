# Tings.co

## What it is

Tings.co is a simple to use, intuitive project management webapp. It was
designed with creatives in mind as it is best used for tracking personal
projects.

Users are able to create new projects, add tasks, give them labels and use these
labels to easily filter through their todo list.

No deadlines, no comment system, no team collaboration features.
Tings focuses only on what's important: **GETTING THINGS DONE**.

## Why it is

I, like many other creatives (Developers, Designers, Content Creators etc) have
personal projects to help me stay motivated and explore new avenues.

The problem is that none of the tools currently available allowed me to track my
projects in a simple way. I used Trello, Todoist, Google Keep and even real
post-it notes without much success.

All I wanted was a place where I can aggregate my projects and tasks, with a
clean and unobtrusive UI. A place to easily add new tings to do and get on with my work.

## The Stack Used

If I'm honest, I also used this opportunity to learn and solifify my knowledge
of the technologies listed below.

The database is PostgreSQL. It's solid and functional. Never had problems
with it.

The Backend is written in Python using Flask. Python because it's my favourite
language. Clean, descriptive and minimal. And Flask for the flexibility and
control it gives me over the code I write.

The Backend essentially acts as a RESTful API that serves JSON to a client
application written in React

I was growing tired of Angular 1.x so I decided it was time to switch things up
and try something new.

The styling is done using sass (the indented flavour).

The app is served behind an Nginx Reverse Proxy.

## The future

Depending on the level of adoption, I have plans to create a cross-platform mobile version and maybe a desktop client using electron.

In terms of devops, I would also like to Dockerise Tings.

When released the app will be free. A paid version will be available in the form
of a subscription plan which will include a few extra goodies and features.

## Notes

The app is currently under heavy developement and is therefore not ready for
prime time yet.

