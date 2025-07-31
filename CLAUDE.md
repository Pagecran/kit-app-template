# NVIDIA Omniverse Kit App Template - Claude Development Guide

This document provides a comprehensive overview of the NVIDIA Omniverse Kit App Template codebase for AI development assistance. It captures the essential information needed to understand, build, and extend applications and extensions within the Omniverse Kit SDK ecosystem.

## Project Overview

The `kit-app-template` is a toolkit for developing GPU-accelerated applications within the NVIDIA Omniverse ecosystem. It provides streamlined tools and templates to create high-performance, OpenUSD-based desktop or cloud streaming applications using the Omniverse Kit SDK.

### Key Features
- **Language Support:** Python and C++ development
- **OpenUSD Foundation:** Built on Open Universal Scene Description (OpenUSD)
- **GPU Acceleration:** Leverages GPU-accelerated capabilities for high-fidelity visualization
- **Extensibility:** Modular extension system with dynamic user interfaces
- **Cross-Platform:** Windows and Linux support
- **Cloud Streaming:** Built-in support for web browser streaming

## Essential Build Commands

### Quick Development Workflow
```bash
# Linux
./repo.sh template new    # Create new app/extension
./repo.sh build          # Build project
./repo.sh launch         # Launch application
./repo.sh test           # Run tests
./repo.sh package        # Package for distribution

# Windows
.\repo.bat template new
.\repo.bat build
.\repo.bat launch
.\repo.bat test
.\repo.bat package
```

### Template Management
```bash
# List available templates
./repo.sh template list

# Create new project interactively
./repo.sh template new

# Add streaming layers to existing app
./repo.sh template modify

# Replay template configuration (for automation)
./repo.sh template new --generate-playbook config.toml
./repo.sh template replay config.toml
```

### Build Options
```bash
# Clean build
./repo.sh build --clean

# Rebuild from scratch
./repo.sh build --rebuild
```

### Launch Options
```bash
# Launch with developer bundle
./repo.sh launch --dev-bundle

# Launch packaged application
./repo.sh launch --package /path/to/package.zip

# Launch containerized app (Linux only)
./repo.sh launch --container

# Pass arguments to Kit executable
./repo.sh launch -- --clear-cache
```

### Package Options
```bash
# Create thin package (registry extensions only)
./repo.sh package --thin

# Create container image (Linux only)
./repo.sh package --container

# Specify package name
./repo.sh package --name my_package_name
```

## Architecture Overview

### Directory Structure
```
kit-app-template/
├── source/                    # User application and extension code
│   ├── apps/                 # Application .kit files
│   └── extensions/           # Custom extensions
├── templates/                # Project templates
│   ├── apps/                # Application templates
│   ├── extensions/          # Extension templates
│   └── templates.toml       # Template configuration
├── tools/                    # Build and packaging tools
├── readme-assets/           # Documentation and assets
├── premake5.lua            # Build configuration
├── repo.toml               # Repository configuration
├── repo.sh / repo.bat      # Main tool entry points
└── .vscode/                # VS Code configuration
```

### Core Configuration Files

#### `repo.toml`
- Repository-level configuration
- Build system settings (Windows C++ compilation disabled by default)
- Extension registry configuration
- Packaging settings
- Template tool configuration

#### `premake5.lua`
- Build script entry point
- Defines applications to build from `source/apps/`
- Currently defines: `pagerender.usd_compose.kit`

#### `templates/templates.toml`
- Defines available project templates
- Maps template names to filesystem locations
- Specifies template variables and dependencies

## Template System

### Application Templates
1. **Kit Base Editor** - Minimal template for OpenUSD content manipulation
2. **USD Composer** - Complex scene authoring application
3. **USD Explorer** - Large scene exploration and collaboration
4. **USD Viewer** - Viewport-only streaming-ready application
5. **Kit Service** - Headless service template

### Extension Templates
1. **Basic Python** - Minimal Python extension
2. **Python UI** - Python extension with user interface
3. **Basic C++** - Minimal C++ extension
4. **Basic C++ w/ Python Bindings** - C++ extension with Python interface via Pybind11
5. **Service Setup** - Service-specific setup extensions

### Application Layer Templates (Streaming)
- **Omniverse Kit App Streaming (Default)**
- **Omniverse Cloud Streaming**
- **GDN Streaming**
- **Omniverse Cloud Streaming (Legacy)**

### Template Variables
Templates use Jinja2-style variable substitution:
- `{{ extension_name }}` - Extension identifier (e.g., `my_company.my_extension`)
- `{{ extension_display_name }}` - Human-readable name
- `{{ application_name }}` - Application identifier
- `{{ application_display_name }}` - Application title
- `{{ version }}` - Semantic version (e.g., `0.1.0`)
- `{{ python_module_path }}` - Python module path

## Extension Configuration

### Extension Structure
```
my_extension/
├── config/
│   └── extension.toml      # Extension metadata and dependencies
├── data/                   # Assets (icons, previews, etc.)
├── docs/                   # Documentation
├── my_extension/           # Python module
│   ├── __init__.py
│   ├── extension.py        # Main extension class
│   └── tests/              # Unit tests
└── premake5.lua           # Build configuration
```

### Extension Configuration (`extension.toml`)
```toml
[package]
title = "My Extension"
version = "0.1.0"
description = "Extension description"
category = "Example"
icon = "data/icon.png"
keywords = ["kit", "example"]

[dependencies]
# Extension dependencies

[[python.module]]
name = "my_company.my_extension"

[[test]]
# Test configuration
```

## Application Configuration

### Kit File Structure (`.kit`)
Kit files are TOML configuration files that define applications by specifying:
- Dependencies (extensions to load)
- Settings (application configuration)
- Window properties (title, icon, size)
- Renderer settings
- Telemetry configuration

### Key Settings Sections
- `[dependencies]` - Required extensions
- `[settings.app]` - Application-level settings
- `[settings.exts."extension.name"]` - Extension-specific settings
- `[settings.persistent.*]` - User-persistent settings
- `[settings.rtx]` - RTX renderer settings

## Testing Framework

### Test Structure
Extensions include test suites using the Kit SDK testing framework:
- Tests inherit from `omni.kit.test.AsyncTestCase`
- Async testing support with `await omni.kit.app.get_app().next_update_async()`
- Startup time and warning count monitoring
- Extension-specific functional tests

### Example Test Pattern
```python
from omni.kit.test import AsyncTestCase

class TestExtension(AsyncTestCase):
    async def test_functionality(self):
        # Wait for app to be ready
        for _ in range(60):
            await omni.kit.app.get_app().next_update_async()
        
        # Test logic here
        self.assertTrue(True)
```

## Development Environment

### VS Code Configuration
The repository includes VS Code configuration:

#### Tasks (`.vscode/tasks.json`)
- **New Template** - Interactive template creation
- **Build** - Build project (default build task)
- **Launch** - Launch application
- **Launch (Developer Mode)** - Launch with developer bundle
- **Run Unit Tests** - Execute test suites
- **Package** - Package application
- **Build All Templates** - Template validation tool

#### Debug Configuration (`.vscode/launch.json`)
- Python remote debugging on port 3000
- Proper path mappings for workspace
- Support for subprocess debugging

### Development Guidelines

#### Extension Naming
- Use company/project prefixed naming: `my_company.my_extension`
- Avoid Python built-in module names (`random`, `sys`, `xml`)
- Use lowercase, alphanumeric, dot-separated identifiers

#### Best Practices
- Extensions are the fundamental building blocks (applications are extension collections)
- One project per repository for production (multiple projects acceptable for experimentation)
- All user code goes in `source/` directory
- Version numbers in `tools/VERSION.md` for packaging

## Platform-Specific Notes

### Windows Development
- C++ compilation disabled by default (`repo.toml`: `"platform:windows-x86_64".enabled = false`)
- Enable C++ by setting `link_host_toolchain = true` in `repo.toml`
- Requires Visual Studio 2019/2022 with C++ workload
- Windows SDK required for C++ development
- Avoid long paths (place repository close to drive root)
- NTFS recommended over exFAT for symlink support

### Linux Development
- Docker support for containerized development
- NVIDIA Container Toolkit for GPU-accelerated containers
- Build essentials package required
- Symlink support required for proper operation

## Performance Considerations

### Startup Times
- Initial RTX renderer launch: 5-8 minutes (shader compilation)
- Subsequent launches: Much faster (compiled shaders cached)
- Use eco mode for development: `rtx.ecoMode.enabled = true`

### Build Optimization
- Use `--clean` flag sparingly (increases build time)
- Thin packages exclude Kit SDK (smaller, faster)
- Fat packages include everything (larger, self-contained)

## Streaming and Deployment

### Streaming Options
1. **Self-Managed:** Omniverse Kit App Streaming on Kubernetes
2. **NVIDIA-Managed:** 
   - Omniverse Cloud (OVC) - Secure, large-scale deployment
   - Graphics Delivery Network (GDN) - Worldwide streaming with URLs

### Container Support
- Linux-only container packaging
- Dockerfile templates in `tools/containers/`
- Entry point scripts for different deployment scenarios
- Memcached support for distributed caching

## Registry and Dependencies

### Extension Registries
Default registries configured in `repo.toml`:
- `kit/default` - Core Kit extensions
- `kit/sdk` - SDK-specific extensions
- `kit/community` - Community extensions

### Version Locking
Applications use version locks for reproducible builds:
- Generated section in `.kit` files
- Kit SDK version: 107.2.0+feature.190796.ae1b1071.gl
- All dependencies locked to specific versions

## Troubleshooting Common Issues

### Build Issues
- Windows path length limitations - place repo near drive root
- exFAT drive issues - use NTFS for proper symlink support
- C++ compilation errors - ensure Visual Studio and Windows SDK installed

### Runtime Issues
- Long startup times - expected on first RTX launch (shader compilation)
- Extension naming conflicts - avoid Python built-in module names
- Memory issues - enable eco mode for development

### Tool Issues
- Use `./repo.sh -h` for help with any tool
- Check `repo.log` in `_repo/` for detailed tool output
- Ensure Git LFS is installed for large file handling

## Key Files for Reference

- `/D/NVIDIA-Omniverse/kit-app-template/README.md` - Main project documentation
- `/D/NVIDIA-Omniverse/kit-app-template/repo.toml` - Repository configuration
- `/D/NVIDIA-Omniverse/kit-app-template/templates/templates.toml` - Template definitions
- `/D/NVIDIA-Omniverse/kit-app-template/readme-assets/additional-docs/kit_app_template_tooling_guide.md` - Detailed tool documentation
- `/D/NVIDIA-Omniverse/kit-app-template/readme-assets/additional-docs/usage_and_troubleshooting.md` - Usage guidelines and troubleshooting

This guide provides the essential information needed to understand and work with the NVIDIA Omniverse Kit App Template codebase effectively.