from app import create_app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, ssl_context=("certs/localhost+2.pem", "certs/localhost+2-key.pem"))