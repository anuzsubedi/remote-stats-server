from flask import Blueprint, jsonify
from src.utils.system_monitor import SystemMonitor

gpu_bp = Blueprint('gpu', __name__)

@gpu_bp.route('/')
def get_all_gpu_info():
    """Get all GPU information including NVIDIA, AMD, integrated, and Raspberry Pi GPUs"""
    try:
        return jsonify(SystemMonitor.get_gpu_info())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gpu_bp.route('/nvidia')
def get_nvidia_gpu_info():
    """Get NVIDIA GPU information"""
    try:
        gpu_info = SystemMonitor.get_gpu_info()
        return jsonify({
            'nvidia': gpu_info.get('nvidia', []),
            'messages': gpu_info.get('messages', []),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gpu_bp.route('/amd')
def get_amd_gpu_info():
    """Get AMD GPU information"""
    try:
        gpu_info = SystemMonitor.get_gpu_info()
        return jsonify({
            'amd': gpu_info.get('amd', []),
            'messages': gpu_info.get('messages', []),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gpu_bp.route('/integrated')
def get_integrated_gpu_info():
    """Get integrated GPU information (Intel, AMD, etc.)"""
    try:
        gpu_info = SystemMonitor.get_gpu_info()
        return jsonify({
            'integrated': gpu_info.get('integrated', []),
            'messages': gpu_info.get('messages', []),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gpu_bp.route('/raspberry-pi')
def get_raspberry_pi_gpu_info():
    """Get Raspberry Pi GPU information"""
    try:
        gpu_info = SystemMonitor.get_gpu_info()
        return jsonify({
            'raspberry_pi': gpu_info.get('raspberry_pi', {}),
            'messages': gpu_info.get('messages', []),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gpu_bp.route('/general')
def get_general_gpu_info():
    """Get general GPU information from system hardware"""
    try:
        gpu_info = SystemMonitor.get_gpu_info()
        return jsonify({
            'general': gpu_info.get('general', {}),
            'messages': gpu_info.get('messages', []),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gpu_bp.route('/opengl')
def get_opengl_info():
    """Get OpenGL information"""
    try:
        gpu_info = SystemMonitor.get_gpu_info()
        return jsonify({
            'opengl': gpu_info.get('opengl', {}),
            'messages': gpu_info.get('messages', []),
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@gpu_bp.route('/messages')
def get_gpu_messages():
    """Get GPU-related messages and status information"""
    try:
        gpu_info = SystemMonitor.get_gpu_info()
        return jsonify({
            'messages': gpu_info.get('messages', []),
            'summary': {
                'nvidia_count': len(gpu_info.get('nvidia', [])),
                'amd_count': len(gpu_info.get('amd', [])),
                'integrated_count': len(gpu_info.get('integrated', [])),
                'raspberry_pi_available': gpu_info.get('raspberry_pi', {}).get('available', False),
                'opengl_available': gpu_info.get('opengl', {}).get('available', False)
            },
            'timestamp': SystemMonitor.get_all_system_info()['timestamp']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 