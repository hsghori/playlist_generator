# Spotify playlist generator

This is a django based single page web app that uses LastFM scrobble data to generate a playlist
baed on your most listened to tracks of the week.

## To launch the application locally:

If you want to run this locally you will need to create LastfM and Spotify apps
- [Create LastFM app](https://www.last.fm/api)
- [Create Spotify app](https://developer.spotify.com/)

Then create a file `secrets.env` of the form:

```
LASTFM_API_KEY=YOUR API KEY
SPOTIFY_API_KEY=YOUR API KEY
SPOTIFY_API_SECRET=YOUR SECRET KEY
SPOTIFY_REDIRECT_URL=http://localhost/auth_callback/
```

These environment variables are loaded by the container when the container is started.

 In a terminal, navigate to the project root and run:
 - `make build` - builds the Docker image
 - `make start` - starts the Docker container and launches the server

(**Optional**) If you plan to change JS or SCSS files open a second terminal and run:
- `make watch` - sets up a watcher job for changes to JS or SCSS

## Useful development commands

The application itself runs inside of a docker container. See the `Makefile` for detailed commands
on building / running the container.

Command                   | Run in the shell? | Description
--------------------------|-------------------|-----------------
`make build`              | No                | Builds the container
`make start`              | No                | Starts the django server
`make shell`              | No                | Opens a shell inside the docker container (to be used to run installation / db config commands)
`make make_migration`     | No                | Creates new migrations
`make migrate`            | Yes               | Runs the database migrations

## Installing a JS library

1. Connect to the docker shell
	```Bash
	make shell
	```
2. Install the package
	```Bash
	npm install <package>
	```
3. Commit the updated `package-lock.json` file.

## Installing a Python library

1. Connect to the docker shell
	```Bash
	make shell
	```
1. Add the library to `requirements.txt`. **Make sure you pin the package version**.
2. Run
    ```Bash
    make python_install
    ```
