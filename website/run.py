from personal_website import app

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)