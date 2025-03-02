from BookStoreApp import init_tables, init_admin, app
if __name__ == '__main__':
    init_tables()
    init_admin()
    app.run(debug=True)
