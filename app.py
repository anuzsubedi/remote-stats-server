from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.routes.system_routes import system_bp
from src.routes.process_routes import process_bp
from src.routes.storage_routes import storage_bp
from src.routes.network_routes import network_bp
from src.routes.gpu_routes import gpu_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(system_bp, url_prefix='/api/system')
    app.register_blueprint(process_bp, url_prefix='/api/processes')
    app.register_blueprint(storage_bp, url_prefix='/api/storage')
    app.register_blueprint(network_bp, url_prefix='/api/network')
    app.register_blueprint(gpu_bp, url_prefix='/api/gpu')
    
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'System monitoring server is running'
        })
    
    @app.route('/api')
    def api_info():
        return jsonify({
            'name': 'System Monitoring API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'system': '/api/system',
                'processes': '/api/processes',
                'storage': '/api/storage',
                'network': '/api/network',
                'gpu': '/api/gpu'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True) 