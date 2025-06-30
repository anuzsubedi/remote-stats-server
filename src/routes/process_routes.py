from flask import Blueprint, jsonify, request
from src.utils.system_monitor import SystemMonitor

process_bp = Blueprint('processes', __name__)

@process_bp.route('/')
def get_all_processes():
    """Get all running processes"""
    try:
        processes = SystemMonitor.get_processes_info()
        return jsonify({
            'processes': processes,
            'count': len(processes),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@process_bp.route('/top')
def get_top_processes():
    """Get top processes by CPU and memory usage"""
    try:
        limit = request.args.get('limit', 10, type=int)
        processes = SystemMonitor.get_processes_info()
        
        # Sort by CPU usage
        top_cpu = sorted(processes, key=lambda x: x.get('cpu_info', {}).get('percent', 0), reverse=True)[:limit]
        
        # Sort by memory usage
        top_memory = sorted(processes, key=lambda x: x.get('memory_info', {}).get('percent', 0), reverse=True)[:limit]
        
        return jsonify({
            'top_cpu': top_cpu,
            'top_memory': top_memory,
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@process_bp.route('/<int:pid>')
def get_process_info(pid):
    """Get information about a specific process"""
    try:
        import psutil
        proc = psutil.Process(pid)
        
        process_info = {
            'pid': proc.pid,
            'name': proc.name(),
            'username': proc.username(),
            'status': proc.status(),
            'create_time': proc.create_time(),
            'cpu_percent': proc.cpu_percent(),
            'memory_percent': proc.memory_percent(),
            'memory_info': {
                'rss': proc.memory_info().rss,
                'vms': proc.memory_info().vms,
                'percent': proc.memory_percent()
            },
            'cpu_info': {
                'percent': proc.cpu_percent(),
                'num_threads': proc.num_threads()
            },
            'connections': [],
            'open_files': [],
            'threads': []
        }
        
        # Get network connections
        try:
            connections = proc.connections()
            for conn in connections:
                process_info['connections'].append({
                    'fd': conn.fd,
                    'family': str(conn.family),
                    'type': str(conn.type),
                    'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    'status': conn.status
                })
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass
        
        # Get open files
        try:
            open_files = proc.open_files()
            for file in open_files:
                process_info['open_files'].append({
                    'path': file.path,
                    'fd': file.fd
                })
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass
        
        # Get threads
        try:
            threads = proc.threads()
            for thread in threads:
                process_info['threads'].append({
                    'id': thread.id,
                    'user_time': thread.user_time,
                    'system_time': thread.system_time
                })
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass
        
        return jsonify(process_info)
    except psutil.NoSuchProcess:
        return jsonify({'error': 'Process not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@process_bp.route('/search')
def search_processes():
    """Search processes by name"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        processes = SystemMonitor.get_processes_info()
        filtered_processes = [
            proc for proc in processes 
            if query in proc.get('name', '').lower()
        ]
        
        return jsonify({
            'processes': filtered_processes,
            'count': len(filtered_processes),
            'query': query,
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 