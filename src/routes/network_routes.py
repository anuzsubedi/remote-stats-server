from flask import Blueprint, jsonify
from src.utils.system_monitor import SystemMonitor

network_bp = Blueprint('network', __name__)

@network_bp.route('/')
def get_all_network_info():
    """Get all network information"""
    try:
        return jsonify(SystemMonitor.get_network_info())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@network_bp.route('/interfaces')
def get_network_interfaces():
    """Get network interfaces information"""
    try:
        network_info = SystemMonitor.get_network_info()
        return jsonify({
            'interfaces': network_info['interfaces'],
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@network_bp.route('/io')
def get_network_io():
    """Get network I/O statistics"""
    try:
        network_info = SystemMonitor.get_network_info()
        return jsonify({
            'io_counters': network_info['io_counters'],
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@network_bp.route('/connections')
def get_network_connections():
    """Get active network connections"""
    try:
        import psutil
        connections = psutil.net_connections()
        
        connection_list = []
        for conn in connections:
            connection_list.append({
                'fd': conn.fd,
                'family': str(conn.family),
                'type': str(conn.type),
                'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                'status': conn.status,
                'pid': conn.pid
            })
        
        return jsonify({
            'connections': connection_list,
            'count': len(connection_list),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 