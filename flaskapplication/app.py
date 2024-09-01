from website import create_app
app = create_app()
# Command : flask run --host=0.0.0.0
if __name__=='__main__':
    app.run(debug=True)