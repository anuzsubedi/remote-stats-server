# System Monitoring API Documentation

## Overview

The System Monitoring API provides comprehensive monitoring capabilities for system resources including CPU, memory, storage, network, processes, and GPU information. All endpoints return JSON responses with timestamps.

**Base URL**: `http://localhost:5000`

## Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

## Response Format

All API responses follow this general format:

```json
{
  "data": "...",
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

## Error Responses

When an error occurs, the API returns an appropriate HTTP status code with an error message:

```json
{
  "error": "Error description"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

---

## Health & Information Endpoints

### Health Check

**GET** `/api/health`

Check if the server is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "message": "System monitoring server is running"
}
```

### API Information

**GET** `/api`

Get information about the API and available endpoints.

**Response:**
```json
{
  "name": "System Monitoring API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/api/health",
    "system": "/api/system",
    "processes": "/api/processes",
    "storage": "/api/storage",
    "network": "/api/network",
    "gpu": "/api/gpu"
  }
}
```

---

## System Information Endpoints

### All System Information

**GET** `/api/system/`

Get comprehensive system information including CPU, memory, disk, network, and GPU data.

**Response:**
```json
{
  "timestamp": "2025-06-30T01:46:47.999739",
  "system": {
    "platform": "Linux",
    "platform_release": "6.12.25+rpt-rpi-2712",
    "platform_version": "#1 SMP PREEMPT Debian 1:6.12.25-1+rpt1 (2025-06-29)",
    "architecture": "aarch64",
    "processor": "aarch64",
    "hostname": "rasp",
    "python_version": "3.11.2",
    "boot_time": 1751252549.0,
    "uptime": 12345.67
  },
  "cpu": {
    "physical_cores": 4,
    "total_cores": 4,
    "max_frequency": 1800000000.0,
    "current_frequency": 1400000000.0,
    "min_frequency": 600000000.0,
    "cpu_usage_percent": 15.2,
    "cpu_usage_per_core": [12.5, 18.3, 14.7, 15.3],
    "temperature": 45.2,
    "cpu_times": {
      "user": 1920.78,
      "system": 734.76,
      "idle": 36600.97,
      "nice": 0.03,
      "iowait": 80.22,
      "irq": 0.0,
      "softirq": 6.13,
      "steal": 0.0,
      "guest": 0.0,
      "guest_nice": 0.0
    },
    "cpu_stats": {
      "ctx_switches": 25953805,
      "interrupts": 12857660,
      "soft_interrupts": 4173136,
      "syscalls": 0
    }
  },
  "memory": {
    "total": 8451194880,
    "available": 5880545280,
    "used": 2142879744,
    "free": 2638266368,
    "percent": 30.4,
    "swap": {
      "total": 536854528,
      "used": 0,
      "free": 536854528,
      "percent": 0.0
    }
  },
  "disk": {
    "partitions": {
      "/dev/mmcblk0p1": {
        "mountpoint": "/boot",
        "filesystem": "vfat",
        "total": 268435456,
        "used": 123456789,
        "free": 144978667,
        "percent": 46.0
      },
      "/dev/mmcblk0p2": {
        "mountpoint": "/",
        "filesystem": "ext4",
        "total": 62730983424,
        "used": 7373256403,
        "free": 52157727021,
        "percent": 11.8
      }
    },
    "io_counters": {
      "read_count": 1234567,
      "write_count": 987654,
      "read_bytes": 123456789012,
      "write_bytes": 98765432109,
      "read_time": 12345,
      "write_time": 9876
    }
  },
  "network": {
    "interfaces": {
      "eth0": {
        "addresses": [
          {
            "family": "17",
            "address": "d8:3a:dd:f3:51:10",
            "netmask": null,
            "broadcast": "ff:ff:ff:ff:ff:ff",
            "ptp": null
          }
        ],
        "stats": {
          "isup": false,
          "duplex": 0,
          "speed": 0,
          "mtu": 1500
        }
      },
      "wlan0": {
        "addresses": [
          {
            "family": "2",
            "address": "192.168.1.100",
            "netmask": "255.255.255.0",
            "broadcast": "192.168.1.255",
            "ptp": null
          }
        ],
        "stats": {
          "isup": true,
          "duplex": 0,
          "speed": 0,
          "mtu": 1500
        }
      }
    },
    "io_counters": {
      "bytes_sent": 123456789012,
      "bytes_recv": 987654321098,
      "packets_sent": 1234567,
      "packets_recv": 9876543,
      "errin": 0,
      "errout": 0,
      "dropin": 0,
      "dropout": 0
    }
  },
  "gpu": {
    "nvidia": [],
    "general": {},
    "opengl": ""
  }
}
```

### General System Information

**GET** `/api/system/general`

Get basic system information like OS, architecture, and hostname.

**Response:**
```json
{
  "platform": "Linux",
  "platform_release": "6.12.25+rpt-rpi-2712",
  "platform_version": "#1 SMP PREEMPT Debian 1:6.12.25-1+rpt1 (2025-06-29)",
  "architecture": "aarch64",
  "processor": "aarch64",
  "hostname": "rasp",
  "python_version": "3.11.2",
  "boot_time": 1751252549.0,
  "uptime": 12345.67
}
```

### CPU Information

**GET** `/api/system/cpu`

Get detailed CPU information including usage, frequency, and statistics.

**Response:**
```json
{
  "physical_cores": 4,
  "total_cores": 4,
  "max_frequency": 1800000000.0,
  "current_frequency": 1400000000.0,
  "min_frequency": 600000000.0,
  "cpu_usage_percent": 15.2,
  "cpu_usage_per_core": [12.5, 18.3, 14.7, 15.3],
  "temperature": 45.2,
  "cpu_times": {
    "user": 1920.78,
    "system": 734.76,
    "idle": 36600.97,
    "nice": 0.03,
    "iowait": 80.22,
    "irq": 0.0,
    "softirq": 6.13,
    "steal": 0.0,
    "guest": 0.0,
    "guest_nice": 0.0
  },
  "cpu_stats": {
    "ctx_switches": 25953805,
    "interrupts": 12857660,
    "soft_interrupts": 4173136,
    "syscalls": 0
  }
}
```

### Memory Information

**GET** `/api/system/memory`

Get memory and swap usage information.

**Response:**
```json
{
  "total": 8451194880,
  "available": 5880545280,
  "used": 2142879744,
  "free": 2638266368,
  "percent": 30.4,
  "swap": {
    "total": 536854528,
    "used": 0,
    "free": 536854528,
    "percent": 0.0
  }
}
```

### Current CPU Usage

**GET** `/api/system/cpu/usage`

Get current CPU usage percentage.

**Response:**
```json
{
  "cpu_usage_percent": 15.2,
  "cpu_usage_per_core": [12.5, 18.3, 14.7, 15.3],
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Current Memory Usage

**GET** `/api/system/memory/usage`

Get current memory usage summary.

**Response:**
```json
{
  "total": 8451194880,
  "used": 2142879744,
  "free": 2638266368,
  "percent": 30.4,
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

---

## Process Monitoring Endpoints

### All Processes

**GET** `/api/processes/`

Get information about all running processes.

**Response:**
```json
{
  "processes": [
    {
      "pid": 1,
      "name": "systemd",
      "username": "root",
      "cpu_percent": 0.0,
      "memory_percent": 0.1411345042844403,
      "status": "sleeping",
      "create_time": 1751252549.0,
      "memory_info": {
        "rss": 11927552,
        "vms": 173473792,
        "percent": 0.1411345042844403
      },
      "cpu_info": {
        "percent": 0.0,
        "num_threads": 1
      }
    }
  ],
  "count": 150,
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Top Processes

**GET** `/api/processes/top?limit={number}`

Get top processes by CPU and memory usage.

**Parameters:**
- `limit` (optional): Number of processes to return (default: 10)

**Example Request:**
```
GET /api/processes/top?limit=5
```

**Response:**
```json
{
  "top_cpu": [
    {
      "pid": 1234,
      "name": "python",
      "username": "user",
      "cpu_percent": 25.5,
      "memory_percent": 2.1,
      "status": "running",
      "create_time": 1751252549.0,
      "memory_info": {
        "rss": 123456789,
        "vms": 987654321,
        "percent": 2.1
      },
      "cpu_info": {
        "percent": 25.5,
        "num_threads": 4
      }
    }
  ],
  "top_memory": [
    {
      "pid": 5678,
      "name": "firefox",
      "username": "user",
      "cpu_percent": 5.2,
      "memory_percent": 15.8,
      "status": "sleeping",
      "create_time": 1751252549.0,
      "memory_info": {
        "rss": 987654321,
        "vms": 1234567890,
        "percent": 15.8
      },
      "cpu_info": {
        "percent": 5.2,
        "num_threads": 25
      }
    }
  ],
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Specific Process Information

**GET** `/api/processes/{pid}`

Get detailed information about a specific process.

**Parameters:**
- `pid`: Process ID

**Example Request:**
```
GET /api/processes/1234
```

**Response:**
```json
{
  "pid": 1234,
  "name": "python",
  "username": "user",
  "status": "running",
  "create_time": 1751252549.0,
  "cpu_percent": 25.5,
  "memory_percent": 2.1,
  "memory_info": {
    "rss": 123456789,
    "vms": 987654321,
    "percent": 2.1
  },
  "cpu_info": {
    "percent": 25.5,
    "num_threads": 4
  },
  "connections": [
    {
      "fd": 3,
      "family": "2",
      "type": "1",
      "laddr": "127.0.0.1:5000",
      "raddr": null,
      "status": "LISTEN"
    }
  ],
  "open_files": [
    {
      "path": "/home/user/file.txt",
      "fd": 4
    }
  ],
  "threads": [
    {
      "id": 1234,
      "user_time": 1.23,
      "system_time": 0.45
    }
  ]
}
```

### Search Processes

**GET** `/api/processes/search?q={query}`

Search for processes by name.

**Parameters:**
- `q` (required): Search query

**Example Request:**
```
GET /api/processes/search?q=python
```

**Response:**
```json
{
  "processes": [
    {
      "pid": 1234,
      "name": "python",
      "username": "user",
      "cpu_percent": 25.5,
      "memory_percent": 2.1,
      "status": "running",
      "create_time": 1751252549.0,
      "memory_info": {
        "rss": 123456789,
        "vms": 987654321,
        "percent": 2.1
      },
      "cpu_info": {
        "percent": 25.5,
        "num_threads": 4
      }
    }
  ],
  "count": 1,
  "query": "python",
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

---

## Storage Monitoring Endpoints

### All Storage Information

**GET** `/api/storage/`

Get comprehensive storage information including partitions and I/O statistics.

**Response:**
```json
{
  "partitions": {
    "/dev/mmcblk0p1": {
      "mountpoint": "/boot",
      "filesystem": "vfat",
      "total": 268435456,
      "used": 123456789,
      "free": 144978667,
      "percent": 46.0
    },
    "/dev/mmcblk0p2": {
      "mountpoint": "/",
      "filesystem": "ext4",
      "total": 62730983424,
      "used": 7373256403,
      "free": 52157727021,
      "percent": 11.8
    }
  },
  "io_counters": {
    "read_count": 1234567,
    "write_count": 987654,
    "read_bytes": 123456789012,
    "write_bytes": 98765432109,
    "read_time": 12345,
    "write_time": 9876
  }
}
```

### Disk Partitions

**GET** `/api/storage/partitions`

Get information about disk partitions.

**Response:**
```json
{
  "partitions": {
    "/dev/mmcblk0p1": {
      "mountpoint": "/boot",
      "filesystem": "vfat",
      "total": 268435456,
      "used": 123456789,
      "free": 144978667,
      "percent": 46.0
    },
    "/dev/mmcblk0p2": {
      "mountpoint": "/",
      "filesystem": "ext4",
      "total": 62730983424,
      "used": 7373256403,
      "free": 52157727021,
      "percent": 11.8
    }
  },
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Disk I/O Statistics

**GET** `/api/storage/io`

Get disk I/O statistics.

**Response:**
```json
{
  "io_counters": {
    "read_count": 1234567,
    "write_count": 987654,
    "read_bytes": 123456789012,
    "write_bytes": 98765432109,
    "read_time": 12345,
    "write_time": 9876
  },
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Disk Usage Summary

**GET** `/api/storage/usage`

Get overall disk usage summary.

**Response:**
```json
{
  "total_space": 62999418880,
  "used_space": 7496712192,
  "free_space": 52308772864,
  "usage_percent": 11.9,
  "partitions_count": 2,
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

---

## Network Monitoring Endpoints

### All Network Information

**GET** `/api/network/`

Get comprehensive network information including interfaces and I/O statistics.

**Response:**
```json
{
  "interfaces": {
    "eth0": {
      "addresses": [
        {
          "family": "17",
          "address": "d8:3a:dd:f3:51:10",
          "netmask": null,
          "broadcast": "ff:ff:ff:ff:ff:ff",
          "ptp": null
        }
      ],
      "stats": {
        "isup": false,
        "duplex": 0,
        "speed": 0,
        "mtu": 1500
      }
    },
    "wlan0": {
      "addresses": [
        {
          "family": "2",
          "address": "192.168.1.100",
          "netmask": "255.255.255.0",
          "broadcast": "192.168.1.255",
          "ptp": null
        }
      ],
      "stats": {
        "isup": true,
        "duplex": 0,
        "speed": 0,
        "mtu": 1500
      }
    }
  },
  "io_counters": {
    "bytes_sent": 123456789012,
    "bytes_recv": 987654321098,
    "packets_sent": 1234567,
    "packets_recv": 9876543,
    "errin": 0,
    "errout": 0,
    "dropin": 0,
    "dropout": 0
  }
}
```

### Network Interfaces

**GET** `/api/network/interfaces`

Get information about network interfaces.

**Response:**
```json
{
  "interfaces": {
    "eth0": {
      "addresses": [
        {
          "family": "17",
          "address": "d8:3a:dd:f3:51:10",
          "netmask": null,
          "broadcast": "ff:ff:ff:ff:ff:ff",
          "ptp": null
        }
      ],
      "stats": {
        "isup": false,
        "duplex": 0,
        "speed": 0,
        "mtu": 1500
      }
    }
  },
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Network I/O Statistics

**GET** `/api/network/io`

Get network I/O statistics.

**Response:**
```json
{
  "io_counters": {
    "bytes_sent": 123456789012,
    "bytes_recv": 987654321098,
    "packets_sent": 1234567,
    "packets_recv": 9876543,
    "errin": 0,
    "errout": 0,
    "dropin": 0,
    "dropout": 0
  },
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Network Connections

**GET** `/api/network/connections`

Get active network connections.

**Response:**
```json
{
  "connections": [
    {
      "fd": 3,
      "family": "2",
      "type": "1",
      "laddr": "127.0.0.1:5000",
      "raddr": null,
      "status": "LISTEN",
      "pid": 1234
    },
    {
      "fd": 4,
      "family": "2",
      "type": "1",
      "laddr": "192.168.1.100:12345",
      "raddr": "192.168.1.1:80",
      "status": "ESTABLISHED",
      "pid": 5678
    }
  ],
  "count": 2,
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

---

## GPU Monitoring Endpoints

### All GPU Information

**GET** `/api/gpu/`

Get all available GPU information, including NVIDIA, AMD, integrated, Raspberry Pi, OpenGL, and general display info.

**Response:**
```json
{
  "nvidia": [
    {
      "name": "NVIDIA GeForce RTX 3080",
      "memory_total": 10240,
      "memory_used": 2048,
      "memory_free": 8192,
      "temperature": 65,
      "utilization": 45,
      "frequency": null
    }
  ],
  "amd": [
    {
      "id": "0",
      "name": "AMD Radeon RX 6800",
      "memory_total": 16384,
      "memory_used": 4096,
      "memory_free": 12288,
      "temperature": 55,
      "utilization": 30,
      "frequency": null
    }
  ],
  "integrated": [
    {
      "name": "Intel UHD Graphics 630",
      "type": "Intel",
      "usage_percent": "25",
      "vendor": "Intel Corporation"
    }
  ],
  "raspberry_pi": {
    "available": true,
    "gpu_memory": "128M",
    "reloc_memory": "0M",
    "malloc_memory": "1M",
    "total_memory": "0M",
    "type": "VideoCore IV",
    "temperature": "temp=45.0'C",
    "frequency": "gpu_freq=500\narm_freq=2400 ...",
    "gpu_freq": 500,
    "gpu_freq_source": "gpu_freq",
    "core_clock": 910007424,
    "v3d_clock": 960009536,
    "isp_clock": 910010752,
    "hevc_clock": 500004288,
    "h264_clock": 0,
    "throttled": "throttled=0xe0000",
    "voltage": "volt=0.8541V"
  },
  "opengl": {
    "available": true,
    "vendor": "NVIDIA Corporation",
    "renderer": "NVIDIA GeForce RTX 3080/PCIe/SSE2",
    "version": "4.6.0 NVIDIA 470.82.01"
  },
  "general": {},
  "messages": []
}
```

#### Field Descriptions
- `nvidia`, `amd`, `integrated`: Arrays of detected GPUs of each type. Each object contains name, memory, temperature, utilization, and frequency (if available).
- `raspberry_pi`: Detailed Raspberry Pi GPU info, including all available memory segments, all available clocks, temperature, throttling, and voltage.
- `opengl`: OpenGL support and renderer info.
- `general`: General display hardware info from lshw.
- `messages`: Any GPU-related status or error messages.

### NVIDIA GPU Information

**GET** `/api/gpu/nvidia`

Get NVIDIA GPU information (if available).

**Response:**
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
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### AMD GPU Information

**GET** `/api/gpu/amd`

Get AMD GPU information (if available).

**Response:**
```json
{
  "amd": [
    {
      "id": "card0",
      "name": "AMD Radeon RX 6800 XT",
      "memory_total": 16384,
      "memory_used": 1024,
      "memory_free": 15360,
      "temperature": 58,
      "utilization": 32
    }
  ],
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Integrated GPU Information

**GET** `/api/gpu/integrated`

Get integrated GPU information (Intel, AMD, etc.).

**Response:**
```json
{
  "integrated": [
    {
      "name": "Intel Integrated GPU",
      "type": "Intel",
      "usage_percent": "15",
      "source": "sysfs"
    },
    {
      "name": "AMD Integrated GPU",
      "type": "AMD",
      "usage_percent": "8",
      "source": "sysfs"
    }
  ],
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### Raspberry Pi GPU Information

**GET** `/api/gpu/raspberry-pi`

Get Raspberry Pi GPU information.

**Response:**
```json
{
  "raspberry_pi": {
    "available": true,
    "gpu_memory": "128M",
    "type": "VideoCore IV",
    "temperature": "temp=45.0'C",
    "frequency": "gpu_freq=500\narm_freq=2400 ...",
    "gpu_freq": 500
  },
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

- `gpu_freq`: The current GPU frequency in MHz, extracted from the config string. If not available, this will be `null`.

### General GPU Information

**GET** `/api/gpu/general`

Get general GPU information from system hardware.

**Response:**
```json
{
  "general": {
    "id": "display:0",
    "class": "display",
    "claimed": true,
    "handle": "PCI:0000:01:00.0",
    "description": "VGA compatible controller",
    "product": "NVIDIA GeForce RTX 3080",
    "vendor": "NVIDIA Corporation",
    "physid": "0",
    "businfo": "pci@0000:01:00.0",
    "version": "a1",
    "width": 64,
    "clock": 1900000000
  },
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### OpenGL Information

**GET** `/api/gpu/opengl`

Get OpenGL information.

**Response:**
```json
{
  "opengl": "OpenGL vendor string: NVIDIA Corporation\nOpenGL renderer string: NVIDIA GeForce RTX 3080/PCIe/SSE2\nOpenGL version string: 4.6.0 NVIDIA 470.82.01",
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

### GPU Messages and Status

**GET** `/api/gpu/messages`

Get GPU-related messages and status information.

**Response:**
```json
{
  "messages": [
    "nvidia-smi not available: [Errno 2] No such file or directory: 'nvidia-smi'",
    "rocm-smi not available: [Errno 2] No such file or directory: 'rocm-smi'",
    "lshw not available: [Errno 2] No such file or directory: 'lshw'",
    "glxinfo not available: [Errno 2] No such file or directory: 'glxinfo'"
  ],
  "summary": {
    "nvidia_count": 0,
    "amd_count": 0,
    "integrated_count": 0,
    "raspberry_pi_available": false,
    "opengl_available": false
  },
  "timestamp": "2025-06-30T01:46:47.999739"
}
```

---

## Usage Examples

### Monitoring Dashboard

Here's an example of how to use the API to create a simple monitoring dashboard:

```bash
# Get all system metrics
curl -s http://localhost:5000/api/system/ | jq '.'

# Get current CPU and memory usage
curl -s http://localhost:5000/api/system/cpu/usage
curl -s http://localhost:5000/api/system/memory/usage

# Get top processes
curl -s http://localhost:5000/api/processes/top?limit=10

# Get disk usage
curl -s http://localhost:5000/api/storage/usage

# Get network statistics
curl -s http://localhost:5000/api/network/io
```

### Automated Monitoring Script

```bash
#!/bin/bash

# Monitor system every 5 seconds
while true; do
    echo "=== System Status $(date) ==="
    
    # CPU Usage
    cpu_usage=$(curl -s http://localhost:5000/api/system/cpu/usage | jq -r '.cpu_usage_percent')
    echo "CPU Usage: ${cpu_usage}%"
    
    # Memory Usage
    mem_usage=$(curl -s http://localhost:5000/api/system/memory/usage | jq -r '.percent')
    echo "Memory Usage: ${mem_usage}%"
    
    # Disk Usage
    disk_usage=$(curl -s http://localhost:5000/api/storage/usage | jq -r '.usage_percent')
    echo "Disk Usage: ${disk_usage}%"
    
    echo "=========================="
    sleep 5
done
```