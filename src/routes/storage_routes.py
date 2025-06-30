from flask import Blueprint, jsonify
from src.utils.system_monitor import SystemMonitor

storage_bp = Blueprint('storage', __name__)

@storage_bp.route('/')
def get_all_storage_info():
    """Get all storage information"""
    try:
        return jsonify(SystemMonitor.get_disk_info())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@storage_bp.route('/partitions')
def get_partitions():
    """Get disk partitions information"""
    try:
        disk_info = SystemMonitor.get_disk_info()
        return jsonify({
            'partitions': disk_info['partitions'],
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@storage_bp.route('/io')
def get_disk_io():
    """Get disk I/O statistics"""
    try:
        disk_info = SystemMonitor.get_disk_info()
        return jsonify({
            'io_counters': disk_info['io_counters'],
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@storage_bp.route('/usage')
def get_disk_usage():
    """Get disk usage summary"""
    try:
        disk_info = SystemMonitor.get_disk_info()
        partitions = disk_info['partitions']
        
        total_space = sum(part['total'] for part in partitions.values())
        used_space = sum(part['used'] for part in partitions.values())
        free_space = sum(part['free'] for part in partitions.values())
        
        return jsonify({
            'total_space': total_space,
            'used_space': used_space,
            'free_space': free_space,
            'usage_percent': (used_space / total_space * 100) if total_space > 0 else 0,
            'partitions_count': len(partitions),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 