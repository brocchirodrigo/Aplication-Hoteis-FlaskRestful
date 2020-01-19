from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'site': [site.json() for site in SiteModel.query.all()]}
    
class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site não encontrado.'}, 404
    
    def post(self, url):
        if SiteModel.find_site(url):
            return {'message': 'O site '"'{0:}'"' já existe.'.format(url)}, 400
        site = SiteModel(url)
        try:
            site.save_site()
        except:
            return {'message': 'Houve um erro ao tentar salvar o site.'}, 500
        return {'message': 'URL '"'{}'"', inserido com sucesso.'.format(url)}
    
    def delete(self, url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {'message': 'Site deleted.'}, 200
        return {'message': 'Site não encontrado.'}, 404