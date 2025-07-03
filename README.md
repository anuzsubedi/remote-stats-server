# System Monitoring API Server



> This API server is designed to be used with the frontend dashboard in [anuzsubedi/remote-stats](https://github.com/anuzsubedi/remote-stats).

---

A comprehensive Flask-based API server for real-time system resource monitoring. Monitor CPU, memory, storage, network, processes, and GPU information with a clean RESTful API.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## System Compatibility & Testing

This API server has been thoroughly tested on:
- **Raspberry Pi 5** running Raspberry Pi OS: All features work as expected, including GPU and CPU temperature monitoring.
- **VMware Fusion VM** on MacBook Pro 2017: Most features work, but GPU monitoring and CPU temperature monitoring are not available in virtualized environments.

For best results, use on native Linux systems or Raspberry Pi hardware.

## Features

### Real-time Monitoring
- **CPU Monitoring**: Usage, frequency, temperature, per-core statistics
- **Memory Monitoring**: RAM and swap usage, detailed memory statistics  
- **Storage Monitoring**: Disk partitions, I/O statistics, usage metrics
- **Network Monitoring**: Interface information, connection statistics
- **Process Monitoring**: Running processes, top processes by CPU/memory
- **GPU Monitoring**: NVIDIA GPU support, AMD GPU support, integrated graphics, Raspberry Pi GPU, OpenGL details

### API Features
- **RESTful Design**: Clean, intuitive API endpoints
- **JSON Responses**: Consistent data format with timestamps
- **CORS Enabled**: Ready for web applications
- **Error Handling**: Comprehensive error responses
- **No Authentication**: Simple setup and usage

### Monitoring Capabilities
- **System Information**: OS, architecture, hostname, uptime
- **Process Details**: CPU/memory usage, connections, open files, threads
- **Storage Analytics**: Partition info, I/O counters, usage summaries
- **Network Stats**: Interface details, connection monitoring, I/O metrics
- **GPU Support**: NVIDIA GPU monitoring, integrated GPU detection, Raspberry Pi VideoCore, OpenGL info

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd remote-stats-server
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**
   ```bash
   python app.py
   ```

The server will be available at `http://localhost:5000`

## Usage

### Basic Usage

```bash
# Check server health
curl http://localhost:5000/api/health

# Get all system information
curl http://localhost:5000/api/system/

# Get current CPU usage
curl http://localhost:5000/api/system/cpu/usage

# Get top 10 processes by memory usage
curl http://localhost:5000/api/processes/top?limit=10

# Get GPU information (all types)
curl http://localhost:5000/api/gpu/
```

### Quick Monitoring Dashboard

```bash
#!/bin/bash
# Simple monitoring script

echo "=== System Status ==="
echo "CPU: $(curl -s http://localhost:5000/api/system/cpu/usage | jq -r '.cpu_usage_percent')%"
echo "Memory: $(curl -s http://localhost:5000/api/system/memory/usage | jq -r '.percent')%"
echo "Disk: $(curl -s http://localhost:5000/api/storage/usage | jq -r '.usage_percent')%"
echo "GPU Messages: $(curl -s http://localhost:5000/api/gpu/messages | jq -r '.messages[]?' | head -1)"
echo "==================="
```

### Python Integration

```python
import requests
import json

# Get system metrics
response = requests.get('http://localhost:5000/api/system/')
data = response.json()

print(f"CPU Usage: {data['cpu']['cpu_usage_percent']}%")
print(f"Memory Usage: {data['memory']['percent']}%")
print(f"Uptime: {data['system']['uptime']} seconds")

# Get GPU information
gpu_response = requests.get('http://localhost:5000/api/gpu/')
gpu_data = gpu_response.json()

if gpu_data['nvidia']:
    print(f"NVIDIA GPUs: {len(gpu_data['nvidia'])}")
if gpu_data['integrated']:
    print(f"Integrated GPUs: {len(gpu_data['integrated'])}")
if gpu_data['raspberry_pi']['available']:
    print("Raspberry Pi GPU detected")
```

## API Documentation

For complete API documentation with all endpoints, request/response examples, and detailed usage instructions, see:

**[API Documentation](API_DOCUMENTATION.md)**

The API documentation includes:
- **20+ API endpoints** with detailed examples
- **Request/response formats** for all endpoints
- **Error handling** and status codes
- **Usage examples** in multiple languages
- **Troubleshooting guide** and best practices

## API Endpoints Overview

| Category | Endpoint | Description |
|----------|----------|-------------|
| **Health** | `/api/health` | Server health status |
| **System** | `/api/system/` | All system information |
| **CPU** | `/api/system/cpu` | CPU details and usage |
| **Memory** | `/api/system/memory` | Memory and swap info |
| **Processes** | `/api/processes/` | All running processes |
| **Storage** | `/api/storage/` | Disk and storage info |
| **Network** | `/api/network/` | Network interfaces and stats |
| **GPU** | `/api/gpu/` | All GPU information |
| **GPU NVIDIA** | `/api/gpu/nvidia` | NVIDIA GPU information |
| **GPU Integrated** | `/api/gpu/integrated` | Integrated GPU information |
| **GPU Raspberry Pi** | `/api/gpu/raspberry-pi` | Raspberry Pi GPU information |
| **GPU OpenGL** | `/api/gpu/opengl` | OpenGL information |
| **GPU Messages** | `/api/gpu/messages` | GPU status messages |

*For complete endpoint details, see [API Documentation](API_DOCUMENTATION.md)*

## Example Responses

### System Health Check
```json
{
  "status": "healthy",
  "message": "System monitoring server is running"
}
```

### CPU Usage
```json
{
  "cpu_usage_percent": 15.2,
  "cpu_usage_per_core": [12.5, 18.3, 14.7, 15.3],
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### GPU Information
```json
{
  "nvidia": [
    {
      "name": "NVIDIA GeForce RTX 3080",
      "memory_total": 10240,
      "memory_used": 2048,
      "memory_free": 8192,
      "temperature": 65,
      "utilization": 45
    }
  ],
  "integrated": [
    {
      "name": "Intel UHD Graphics 630",
      "vendor": "Intel Corporation",
      "type": "Intel",
      "usage_percent": "25"
    }
  ],
  "raspberry_pi": {
    "available": true,
    "gpu_memory": "128M",
    "type": "VideoCore IV",
    "temperature": "temp=45.0'C",
    "frequency": "gpu_freq=500\narm_freq=2400 ...",
    "gpu_freq": 500,
    "reloc_memory": "128M",
    "malloc_memory": "128M",
    "total_memory": "256M",
    "core_clock": 500,
    "v3d_clock": 500,
    "isp_clock": 500,
    "hevc_clock": 500,
    "h264_clock": 500,
    "throttled": "0x0",
    "voltage": "1.2V"
  },
  "opengl": {
    "available": true,
    "vendor": "NVIDIA Corporation",
    "renderer": "NVIDIA GeForce RTX 3080/PCIe/SSE2",
    "version": "4.6.0 NVIDIA 470.82.01"
  },
  "messages": []
}
```

- `gpu_freq`: The current GPU frequency in MHz, extracted from the config string. If not available, this will be `null`.
- `reloc_memory`, `malloc_memory`, `total_memory`: Additional Raspberry Pi GPU memory segments.
- `core_clock`, `v3d_clock`, `isp_clock`, `hevc_clock`, `h264_clock`: All available GPU clocks in Hz.
- `throttled`: Throttling status from vcgencmd.
- `voltage`: Measured GPU voltage.

See the [API Documentation](API_DOCUMENTATION.md) for a full list of fields and example responses for all GPU types.

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_DEBUG`: Set to `0` to disable debug mode

### Port Configuration
The server runs on port 5000 by default. To change the port, modify `app.py`:

```python
app.run(host='0.0.0.0', port=8080, debug=True)  # Change port to 8080
```

## Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (Gunicorn, uWSGI)
2. **Set up reverse proxy** (Nginx, Apache)
3. **Enable authentication** if needed
4. **Configure logging** and monitoring
5. **Set up SSL/TLS** for secure connections

### Example with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Development

### Running in Development Mode
```bash
source venv/bin/activate
python app.py
```

### Adding New Endpoints
1. Create a new route file in `src/routes/`
2. Import and register the blueprint in `app.py`
3. Update the API documentation

### Testing Endpoints
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test system endpoint
curl http://localhost:5000/api/system/cpu

# Test GPU endpoints
curl http://localhost:5000/api/gpu/
curl http://localhost:5000/api/gpu/messages

# Test with jq for pretty output
curl -s http://localhost:5000/api/system/memory | jq '.'
```

## Requirements

### Python Dependencies
- **Flask** (2.3.3) - Web framework
- **Flask-CORS** (4.0.0) - Cross-origin resource sharing
- **psutil** (5.9.6) - System and process utilities
- **Werkzeug** (2.3.7) - WSGI utilities

### System Dependencies (Optional)
- **nvidia-smi** - For NVIDIA GPU monitoring (requires NVIDIA GPU and drivers)
- **rocm-smi** - For AMD GPU monitoring (requires AMD ROCm drivers)
- **radeontop** - Alternative AMD GPU monitoring tool
- **lshw** - For general hardware information
- **glxinfo** - For OpenGL information (part of mesa-utils package)
- **vcgencmd** - For Raspberry Pi GPU monitoring (included with Raspberry Pi OS)

### Installation Commands
```bash
# Ubuntu/Debian
sudo apt install lshw mesa-utils

# CentOS/RHEL
sudo yum install lshw mesa-utils

# macOS
brew install lshw

# NVIDIA GPU monitoring (if you have NVIDIA GPU)
# Install NVIDIA drivers and nvidia-smi will be available

# AMD GPU monitoring (if you have AMD GPU)
# Install AMD ROCm drivers and rocm-smi will be available
# Alternative: sudo apt install radeontop
```

## Troubleshooting

### Common Issues

**Server won't start**
```bash
# Check if port is in use
lsof -i :5000

# Check Python version
python --version
```

**Permission errors**
```bash
# Some endpoints require elevated privileges
sudo python app.py
```

**Missing GPU information**
```bash
# Install required tools
sudo apt install lshw mesa-utils

# For NVIDIA GPU monitoring, ensure NVIDIA drivers are installed
# For AMD GPU monitoring, ensure AMD ROCm drivers are installed
# Alternative AMD monitoring: sudo apt install radeontop
# For Raspberry Pi, ensure you're running Raspberry Pi OS
```

**GPU monitoring not working**
```bash
# Check GPU messages endpoint for specific issues
curl http://localhost:5000/api/gpu/messages

# Common solutions:
# - Install missing system tools (lshw, mesa-utils)
# - Install NVIDIA drivers for NVIDIA GPUs
# - Ensure X11 is running for OpenGL info
# - Check if running on Raspberry Pi for VideoCore GPU
```

### Debug Mode
The server runs in debug mode by default. Check console output for detailed error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **psutil** - For comprehensive system monitoring capabilities
- **Flask** - For the excellent web framework
- **Linux community** - For system monitoring tools and documentation

## Environment Variables & .env Usage

This backend uses a `.env` file for configuration. You can set the following variables:

```
PORT=5000
FLASK_DEBUG=True
CORS_ALLOWED_ORIGINS=*
```

- `PORT`: The port the Flask server will run on (default: 5000)
- `FLASK_DEBUG`: Set to `True` for debug mode, `False` for production
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS (default: `*` for all origins)

**How to use:**
1. Copy the sample above into a file named `.env` in the backend root directory.
2. The server will automatically load these settings on startup.

---