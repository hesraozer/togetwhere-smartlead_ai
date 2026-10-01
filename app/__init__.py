import os

from flask import Flask
from flask_cors import CORS

from config import config
from app.database import init_db


def create_app():
    """Flask uygulamasini olusturur ve gerekli parcalari birbirine baglar."""

    app = Flask(__name__)

    ortam = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(ortam, config['default']))

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config['CORS_ORIGINS']
            }
        }
    )

    init_db(app)

    from app.routes import pages_bp, api_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/health')
    def health():
        return {'durum': 'aktif'}, 200

    return app