from flask import Blueprint, jsonify
from src.utils.system_monitor import SystemMonitor

system_bp = Blueprint('system', __name__)

@system_bp.route('/')
def get_all_system_info():
    """Get all system information"""
    try:
        return jsonify(SystemMonitor.get_all_system_info())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_bp.route('/general')
def get_general_system_info():
    """Get general system information"""
    try:
        return jsonify(SystemMonitor.get_system_info())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_bp.route('/cpu')
def get_cpu_info():
    """Get CPU information"""
    try:
        return jsonify(SystemMonitor.get_cpu_info())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_bp.route('/memory')
def get_memory_info():
    """Get memory information"""
    try:
        return jsonify(SystemMonitor.get_memory_info())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_bp.route('/cpu/usage')
def get_cpu_usage():
    """Get current CPU usage"""
    try:
        cpu_info = SystemMonitor.get_cpu_info()
        return jsonify({
            'cpu_usage_percent': cpu_info['cpu_usage_percent'],
            'cpu_usage_per_core': cpu_info['cpu_usage_per_core'],
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@system_bp.route('/memory/usage')
def get_memory_usage():
    """Get current memory usage"""
    try:
        memory_info = SystemMonitor.get_memory_info()
        return jsonify({
            'total': memory_info['total'],
            'used': memory_info['used'],
            'free': memory_info['free'],
            'percent': memory_info['percent'],
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 