import psutil
import platform
import os
import subprocess
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

class SystemMonitor:
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """Get comprehensive CPU information"""
        cpu_info = {
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'max_frequency': psutil.cpu_freq().max if psutil.cpu_freq() else None,
            'current_frequency': psutil.cpu_freq().current if psutil.cpu_freq() else None,
            'min_frequency': psutil.cpu_freq().min if psutil.cpu_freq() else None,
            'cpu_usage_percent': psutil.cpu_percent(interval=1),
            'cpu_usage_per_core': psutil.cpu_percent(interval=1, percpu=True),
            'cpu_times': {
                'user': psutil.cpu_times().user,
                'system': psutil.cpu_times().system,
                'idle': psutil.cpu_times().idle,
                'nice': psutil.cpu_times().nice,
                'iowait': psutil.cpu_times().iowait,
                'irq': psutil.cpu_times().irq,
                'softirq': psutil.cpu_times().softirq,
                'steal': psutil.cpu_times().steal,
                'guest': psutil.cpu_times().guest,
                'guest_nice': psutil.cpu_times().guest_nice
            },
            'cpu_stats': {
                'ctx_switches': psutil.cpu_stats().ctx_switches,
                'interrupts': psutil.cpu_stats().interrupts,
                'soft_interrupts': psutil.cpu_stats().soft_interrupts,
                'syscalls': psutil.cpu_stats().syscalls
            }
        }
        
        # Get CPU temperature if available
        try:
            cpu_temp = SystemMonitor._get_cpu_temperature()
            if cpu_temp:
                cpu_info['temperature'] = cpu_temp
        except:
            pass
            
        return cpu_info
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Get comprehensive memory information"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'free': memory.free,
            'percent': memory.percent,
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            }
        }
    
    @staticmethod
    def get_disk_info() -> Dict[str, Any]:
        """Get comprehensive disk information"""
        disk_partitions = psutil.disk_partitions()
        disk_usage = {}
        disk_io = psutil.disk_io_counters()
        
        for partition in disk_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.device] = {
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            except PermissionError:
                continue
        
        return {
            'partitions': disk_usage,
            'io_counters': {
                'read_count': disk_io.read_count if disk_io else 0,
                'write_count': disk_io.write_count if disk_io else 0,
                'read_bytes': disk_io.read_bytes if disk_io else 0,
                'write_bytes': disk_io.write_bytes if disk_io else 0,
                'read_time': disk_io.read_time if disk_io else 0,
                'write_time': disk_io.write_time if disk_io else 0
            } if disk_io else {}
        }
    
    @staticmethod
    def get_network_info() -> Dict[str, Any]:
        """Get comprehensive network information"""
        network_io = psutil.net_io_counters()
        network_interfaces = psutil.net_if_addrs()
        network_stats = psutil.net_if_stats()
        
        interfaces = {}
        for interface_name, interface_addresses in network_interfaces.items():
            interfaces[interface_name] = {
                'addresses': [],
                'stats': {}
            }
            
            for address in interface_addresses:
                interfaces[interface_name]['addresses'].append({
                    'family': str(address.family),
                    'address': address.address,
                    'netmask': address.netmask,
                    'broadcast': address.broadcast,
                    'ptp': address.ptp
                })
            
            if interface_name in network_stats:
                stats = network_stats[interface_name]
                interfaces[interface_name]['stats'] = {
                    'isup': stats.isup,
                    'duplex': stats.duplex,
                    'speed': stats.speed,
                    'mtu': stats.mtu
                }
        
        return {
            'interfaces': interfaces,
            'io_counters': {
                'bytes_sent': network_io.bytes_sent,
                'bytes_recv': network_io.bytes_recv,
                'packets_sent': network_io.packets_sent,
                'packets_recv': network_io.packets_recv,
                'errin': network_io.errin,
                'errout': network_io.errout,
                'dropin': network_io.dropin,
                'dropout': network_io.dropout
            }
        }
    
    @staticmethod
    def get_processes_info() -> List[Dict[str, Any]]:
        """Get information about all running processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
            try:
                proc_info = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status', 'create_time'])
                proc_info['memory_info'] = {
                    'rss': proc.memory_info().rss,
                    'vms': proc.memory_info().vms,
                    'percent': proc.memory_percent()
                }
                proc_info['cpu_info'] = {
                    'percent': proc.cpu_percent(),
                    'num_threads': proc.num_threads()
                }
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return processes
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get general system information"""
        # Get processor information
        processor = platform.processor()
        if not processor:
            # Try to get processor info from /proc/device-tree/model (common on ARM systems)
            try:
                with open('/proc/device-tree/model', 'r') as f:
                    processor = f.read().strip().replace('\x00', '')
            except (FileNotFoundError, PermissionError):
                # Fallback to architecture-based naming
                arch = platform.machine()
                if arch == 'aarch64':
                    processor = 'ARM64 Processor'
                elif arch == 'armv7l':
                    processor = 'ARMv7 Processor'
                elif arch == 'armv6l':
                    processor = 'ARMv6 Processor'
                else:
                    processor = f'{arch} Processor'
        
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': processor,
            'hostname': platform.node(),
            'python_version': platform.python_version(),
            'boot_time': psutil.boot_time(),
            'uptime': time.time() - psutil.boot_time()
        }
    
    @staticmethod
    def get_gpu_info() -> Dict[str, Any]:
        """Get GPU information using various methods"""
        gpu_info = {}
        
        # Try nvidia-smi for NVIDIA GPUs
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu,utilization.gpu', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                gpu_info['nvidia'] = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(', ')
                        if len(parts) >= 6:
                            gpu_info['nvidia'].append({
                                'name': parts[0],
                                'memory_total': int(parts[1]),
                                'memory_used': int(parts[2]),
                                'memory_free': int(parts[3]),
                                'temperature': int(parts[4]),
                                'utilization': int(parts[5])
                            })
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        # Try rocm-smi for AMD GPUs
        try:
            result = subprocess.run(['rocm-smi', '--showproductname', '--showmeminfo', 'vram', '--showtemp', '--showuse', '--json'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                gpu_info['amd'] = []
                try:
                    amd_data = json.loads(result.stdout)
                    for gpu_id, gpu_data in amd_data.items():
                        if isinstance(gpu_data, dict):
                            gpu_info['amd'].append({
                                'id': gpu_id,
                                'name': gpu_data.get('Card SKU', 'Unknown'),
                                'memory_total': gpu_data.get('vram', {}).get('Total Memory (B)', 0),
                                'memory_used': gpu_data.get('vram', {}).get('Used Memory (B)', 0),
                                'memory_free': gpu_data.get('vram', {}).get('Free Memory (B)', 0),
                                'temperature': gpu_data.get('Temperature (Sensor edge) (C)', 0),
                                'utilization': gpu_data.get('GPU use (%)', 0)
                            })
                except json.JSONDecodeError:
                    # Fallback to parsing text output
                    lines = result.stdout.strip().split('\n')
                    current_gpu = {}
                    for line in lines:
                        if 'Card SKU' in line:
                            if current_gpu:
                                gpu_info['amd'].append(current_gpu)
                            current_gpu = {'name': line.split(':')[-1].strip()}
                        elif 'Total Memory' in line:
                            current_gpu['memory_total'] = str(int(line.split(':')[-1].strip().split()[0]))
                        elif 'Used Memory' in line:
                            current_gpu['memory_used'] = str(int(line.split(':')[-1].strip().split()[0]))
                        elif 'Temperature' in line:
                            current_gpu['temperature'] = str(int(line.split(':')[-1].strip().split()[0]))
                        elif 'GPU use' in line:
                            current_gpu['utilization'] = str(int(line.split(':')[-1].strip().split('%')[0]))
                    if current_gpu:
                        gpu_info['amd'].append(current_gpu)
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        # Try radeontop for AMD GPU monitoring (alternative method)
        try:
            result = subprocess.run(['radeontop', '-d', '-', '-l', '1'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and not gpu_info.get('amd'):
                # Parse radeontop output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'gpu' in line.lower() and '%' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            gpu_info.setdefault('amd', []).append({
                                'name': 'AMD GPU (radeontop)',
                                'utilization': int(parts[1].replace('%', '')),
                                'source': 'radeontop'
                            })
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        # Try lshw for general GPU info
        try:
            result = subprocess.run(['lshw', '-class', 'display', '-json'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                gpu_info['general'] = json.loads(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError, json.JSONDecodeError):
            pass
        
        # Try glxinfo for OpenGL info
        try:
            result = subprocess.run(['glxinfo', '-B'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                gpu_info['opengl'] = result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            pass
        
        # Try vcgencmd for Raspberry Pi GPU
        try:
            result = subprocess.run(['vcgencmd', 'get_mem', 'gpu'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                gpu_memory = result.stdout.strip()
                pi_gpu = {
                    'available': True,
                    'gpu_memory': gpu_memory,
                    'type': 'VideoCore IV'
                }
                # Add all get_mem segments
                for mem_type in ['reloc', 'malloc', 'total']:
                    try:
                        mem_result = subprocess.run(['vcgencmd', 'get_mem', mem_type], capture_output=True, text=True, timeout=2)
                        if mem_result.returncode == 0:
                            pi_gpu[f'{mem_type}_memory'] = mem_result.stdout.strip()
                    except:
                        pi_gpu[f'{mem_type}_memory'] = None
                # Add all measure_clock outputs
                for clk in ['core', 'v3d', 'isp', 'hevc', 'h264']:
                    try:
                        clk_result = subprocess.run(['vcgencmd', 'measure_clock', clk], capture_output=True, text=True, timeout=2)
                        if clk_result.returncode == 0:
                            val = clk_result.stdout.strip()
                            match = re.search(r'frequency\(0\)=([0-9]+)', val)
                            pi_gpu[f'{clk}_clock'] = int(match.group(1)) if match else val
                    except:
                        pi_gpu[f'{clk}_clock'] = None
                # Add temperature
                try:
                    temp_result = subprocess.run(['vcgencmd', 'measure_temp'], 
                                               capture_output=True, text=True, timeout=2)
                    if temp_result.returncode == 0:
                        pi_gpu['temperature'] = temp_result.stdout.strip()
                except:
                    pi_gpu['temperature'] = None
                # Add throttling info
                try:
                    throttled_result = subprocess.run(['vcgencmd', 'get_throttled'], capture_output=True, text=True, timeout=2)
                    if throttled_result.returncode == 0:
                        pi_gpu['throttled'] = throttled_result.stdout.strip()
                except:
                    pi_gpu['throttled'] = None
                # Add voltage info
                try:
                    volts_result = subprocess.run(['vcgencmd', 'measure_volts'], capture_output=True, text=True, timeout=2)
                    if volts_result.returncode == 0:
                        pi_gpu['voltage'] = volts_result.stdout.strip()
                except:
                    pi_gpu['voltage'] = None
                # Add frequency config
                try:
                    freq_result = subprocess.run(['vcgencmd', 'get_config', 'int', 'gpu_freq'], 
                                               capture_output=True, text=True, timeout=2)
                    if freq_result.returncode == 0:
                        freq_config = freq_result.stdout.strip()
                        pi_gpu['frequency'] = freq_config
                        match = re.search(r'gpu_freq=([0-9]+)', freq_config)
                        if match:
                            pi_gpu['gpu_freq'] = int(match.group(1))
                        else:
                            # Fallback: try core_freq, v3d_freq, hevc_freq
                            core_match = re.search(r'core_freq=([0-9]+)', freq_config)
                            v3d_match = re.search(r'v3d_freq=([0-9]+)', freq_config)
                            hevc_match = re.search(r'hevc_freq=([0-9]+)', freq_config)
                            if core_match:
                                pi_gpu['gpu_freq'] = int(core_match.group(1))
                                pi_gpu['gpu_freq_source'] = 'core_freq'
                            elif v3d_match:
                                pi_gpu['gpu_freq'] = int(v3d_match.group(1))
                                pi_gpu['gpu_freq_source'] = 'v3d_freq'
                            elif hevc_match:
                                pi_gpu['gpu_freq'] = int(hevc_match.group(1))
                                pi_gpu['gpu_freq_source'] = 'hevc_freq'
                            else:
                                pi_gpu['gpu_freq'] = None
                                pi_gpu['gpu_freq_source'] = None
                except:
                    pi_gpu['frequency'] = None
                gpu_info['raspberry_pi'] = pi_gpu
            else:
                gpu_info['raspberry_pi'] = {'available': False}
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            gpu_info['raspberry_pi'] = {'available': False}
        
        # Check for Intel integrated GPU info
        try:
            if os.path.exists('/sys/class/drm/card0/device/gpu_busy_percent'):
                with open('/sys/class/drm/card0/device/gpu_busy_percent', 'r') as f:
                    intel_gpu_usage = f.read().strip()
                    gpu_info.setdefault('integrated', []).append({
                        'name': 'Intel Integrated GPU',
                        'type': 'Intel',
                        'usage_percent': intel_gpu_usage,
                        'source': 'sysfs'
                    })
        except:
            pass
        
        # Check for AMD integrated GPU info
        try:
            if os.path.exists('/sys/class/drm/card0/device/gpu_busy_percent'):
                with open('/sys/class/drm/card0/device/gpu_busy_percent', 'r') as f:
                    amd_gpu_usage = f.read().strip()
                    gpu_info.setdefault('integrated', []).append({
                        'name': 'AMD Integrated GPU',
                        'type': 'AMD',
                        'usage_percent': amd_gpu_usage,
                        'source': 'sysfs'
                    })
        except:
            pass
        
        # Add frequency field for NVIDIA GPUs if possible
        if 'nvidia' in gpu_info:
            for gpu in gpu_info['nvidia']:
                # Try to get frequency via nvidia-smi (not available in default query)
                gpu['frequency'] = None  # nvidia-smi does not provide frequency in this call
                # Optionally, run nvidia-smi -q -d CLOCK for more details (not implemented for speed)

        # Add frequency field for AMD GPUs if possible
        if 'amd' in gpu_info:
            for gpu in gpu_info['amd']:
                gpu['frequency'] = None  # rocm-smi parsing not implemented for frequency

        # For integrated GPUs, add vendor if available
        if 'integrated' in gpu_info:
            for gpu in gpu_info['integrated']:
                if 'type' in gpu and gpu['type'] == 'Intel':
                    gpu['vendor'] = 'Intel Corporation'
                elif 'type' in gpu and gpu['type'] == 'AMD':
                    gpu['vendor'] = 'Advanced Micro Devices, Inc.'
                else:
                    gpu['vendor'] = 'Unknown'

        # Comments added for clarity and maintainability
        return gpu_info
    
    @staticmethod
    def _get_cpu_temperature() -> Optional[float]:
        """Get CPU temperature from various sources"""
        # Try different temperature sources
        temp_sources = [
            '/sys/class/thermal/thermal_zone0/temp',
            '/sys/class/hwmon/hwmon0/temp1_input',
            '/sys/class/hwmon/hwmon1/temp1_input',
            '/proc/acpi/thermal_zone/THM0/temperature'
        ]
        
        for source in temp_sources:
            try:
                with open(source, 'r') as f:
                    temp = float(f.read().strip())
                    # Convert from millidegrees to degrees Celsius
                    if temp > 1000:
                        temp /= 1000
                    return temp
            except (FileNotFoundError, ValueError, PermissionError):
                continue
        
        return None
    
    @staticmethod
    def get_all_system_info() -> Dict[str, Any]:
        """Get all system information in one call"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system': SystemMonitor.get_system_info(),
            'cpu': SystemMonitor.get_cpu_info(),
            'memory': SystemMonitor.get_memory_info(),
            'disk': SystemMonitor.get_disk_info(),
            'network': SystemMonitor.get_network_info(),
            'gpu': SystemMonitor.get_gpu_info()
        } 