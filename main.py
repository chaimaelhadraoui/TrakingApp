# main.py
from . import db, cursor
from flask import Blueprint, render_template, redirect, url_for, request,flash

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/search')
def search_rederict():
    return redirect(url_for('main.search'))


@main.route('/search', methods=["POST"])
def search():
    try:
        # Bordreau details
        code = request.form.get('searchCode', type=str)
        print(code)
        query = "SELECT * FROM mes_bordeau where code = %s;" % code
        cursor.execute(query)
        bordreau = cursor.fetchone()
        print(bordreau)

        # Product details
        query = "SELECT * FROM bor_pro where id_bor = {}".format(1)
        cursor.execute(query)
        bor_pro = tuple(cursor.fetchall())
        produits = []
        for id_produit in bor_pro:
            query = "SELECT * FROM mes_produit where id_Produit={}".format(id_produit[2])
            cursor.execute(query)
            produit = tuple(cursor)
            produits.append(produit)

        # Date depot
        query = "SELECT * from date where id_date={} ".format(bordreau[1])
        cursor.execute(query)
        date = cursor.fetchone()[0]

        # Comments
        query = "SELECT * from comment where id_bordreau={} ".format(bordreau[9])
        cursor.execute(query)
        comments = tuple(cursor)

        return render_template('search.html/', produits=produits[0], bordreau=bordreau, date=date, comments=comments)
    except:
        flash("Votre code n'existe pas ",'danger')
        return render_template('index.html')

@main.route('/details/bordreau=<string:id_bordreau>&code=<string:code>', methods=['GET'])
def details(id_bordreau, code):
    # Get Operations from db
    query = 'SELECT * FROM mes_op WHERE id_bord = {}'.format(id_bordreau)
    cursor.execute(query)
    operationsTuple = tuple(cursor)
    operations = []
    for operation in operationsTuple:
        print(operation)
        # Get libelle and date of opertion
        query = 'SELECT libelle,date.date FROM mes_prm_operation,date  where  mes_prm_operation.id_prm_op= {} and date.id_date = {} order by date.date ;'.format(
            operation[2], operation[3])
        cursor.execute(query)
        operationElement = list(cursor.fetchone())
        operationElement.append(operation[4])
        operations.append(operationElement)

    return render_template('details.html', code=code, operations=enumerate(operations, 1))


@main.route('/details/bordreau=<string:code>')
def details_rederict(code):
    return redirect(url_for('main.details'))
