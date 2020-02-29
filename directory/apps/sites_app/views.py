from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from directory import db
from directory.utils.request import json_only

from . import sites
from .models import Site


@sites.route('/', methods=['POST'])
@json_only
@jwt_required
def create_site():
    args = request.get_json()
    try:
        new_site = Site()
        new_site.name = args.get('name')
        new_site.description = args.get('description')
        new_site.address = args.get('address')
        db.session.add(new_site)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return {'error': f'{e}'}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Address is duplicated.'}, 400
    return {'message': 'Site added successfully', 'id': new_site.id}, 201


@sites.route('/', methods=['GET'])
def read_sites():
    sites = Site.query.all()
    sites = [
        {
            'id': site.id,
            'name': site.name,
            'address': site.address,
            'site': url_for('static', filename=site.icon, _external=True) if site.icon else None
        } for site in sites
    ]
    return jsonify(sites), 200


@sites.route('/<int:site_id>/', methods=['GET'])
def read_site(site_id):
    site = Site.query.get(site_id)
    if not site:
        return {'error': 'Site with given ID not found!'}, 404
    return {'id': site.id,
            'create_date': site.create_date,
            'name': site.name,
            'description': site.description,
            'address': site.address,
            'icon': url_for('static', filename=site.icon, _external=True) if site.icon else None}, 200


@sites.route('/<int:site_id>/icon', methods=['PATCH'])
@jwt_required
def modify_thumbnail(site_id):
    site = Site.query.get(site_id)
    if not site:
        return {'error': 'Site with given ID not found!'}, 404
    file = request.files.get('file')
    if not file:
        return {'error': 'File cant be null!'}, 400
    filename = secure_filename(file.filename)
    file.save(f'directory/static/{filename}')
    site.icon = filename
    db.session.commit()
    return {}, 204


@sites.route('/<int:site_id>/', methods=['PATCH'])
@jwt_required
def modify_site(site_id):
    args = request.get_json()
    site = Site.query.get(site_id)
    if not site:
        return {'error': 'Site with given ID not found!'}, 404

    try:
        site.name = args.get('name') if args.get('name') else site.name
        site.description = args.get('description') if args.get('description') else site.description
        site.address = args.get('address') if args.get('address') else site.address
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return {'error': f'{e}'}, 400

    return {}, 204
    

@sites.route('/<int:site_id>/', methods=['DELETE'])
@jwt_required
def delete_site(site_id):
    site = Site.query.get(site_id)
    if not site:
        return {'error': 'Site with given ID not found!'}, 404
    
    db.session.delete(site)
    db.session.commit()
    return {}, 204
    