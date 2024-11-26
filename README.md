# ubiquitous-octo-fortnight
A comprehensive automation tool that sets up a complete Android development environment and creates ready-to-use Android projects, supporting both Java and Python-based development. Perfect for developers who want to quickly start Android development without manual setup hassles.

## 🌟 Key Features

- **Automated Environment Setup**
  - Java Development Kit (OpenJDK 17)
  - Android SDK and NDK
  - Gradle Build System
  - Environment variables configuration

- **Multi-Language Support**
  - Java-based Android development (traditional)
  - Python-based development with Kivy
  - Buildozer integration for Python apps

- **Project Templates**
  - Java Android app template with Material Design
  - Kivy app template with modern UI
  - Ready-to-use project structures

- **Cross-Platform**
  - Windows support with automated Java installation
  - macOS/Linux compatibility
  - Platform-specific optimizations

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- curl (for downloading components)
- Internet connection
- ~10GB free disk space
- Administrator privileges (for system-wide installations)

## 🚀 Quick Start

1. Clone this repository or download the script
2. Open a terminal/command prompt
3. Navigate to the script directory
4. Run:
   ```bash
   python setup_android_env.py
   ```

The script will automatically:
1. Install OpenJDK 17 (if needed)
2. Set up Android SDK
3. Install Gradle
4. Create sample projects

## 📦 Components Installed

### Core Components
- OpenJDK 17
- Android SDK Platform-tools
- Android SDK Build-tools 31.0.0
- Android Platform API 31
- Android NDK 25.2.9519653
- Gradle 8.4

### Python Development Tools
- Buildozer (Python-to-Android packaging)
- Kivy (Python UI framework)
- Cython (for native performance)

## 🎯 Project Types

### Java Android Project (MyJavaApp)
- Modern Android architecture
- Material Design components
- AndroidX libraries
- Gradle build system
- Ready for Android Studio

### Python Kivy Project (MyKivyApp)
- Cross-platform UI
- Hot reload support
- Simple and intuitive API
- Buildozer configuration
- Quick prototyping

## 🛠️ Building Projects

### Java Project
```bash
cd MyJavaApp
./gradlew build          # Build the project
./gradlew installDebug   # Install on device
```

### Python Project
```bash
cd MyKivyApp
buildozer init          # Initialize buildozer
buildozer android debug # Build APK
```

## 🌍 Environment Setup

The script configures:
- JAVA_HOME
- ANDROID_HOME
- GRADLE_HOME
- PATH updates
- SDK licenses

## 🔧 Troubleshooting Guide

### Common Issues

1. **Java Installation Fails**
   - Download OpenJDK 17 manually
   - Set JAVA_HOME manually
   - Verify with `java -version`

2. **SDK Installation Issues**
   - Check internet connection
   - Run as administrator
   - Clear temp files and retry
   - Verify Android SDK licenses

3. **Gradle Problems**
   - Check GRADLE_HOME
   - Clear Gradle cache
   - Run with `--stacktrace`

4. **Python/Buildozer Issues**
   - Update pip: `python -m pip install --upgrade pip`
   - Install Buildozer deps: `pip install --upgrade buildozer`
   - Check Cython installation

### Verification Steps

```bash
# Verify Java
java -version

# Verify Android tools
adb version
sdkmanager --list

# Verify Gradle
gradle -v

# Verify Python tools
python -c "import kivy; print(kivy.__version__)"
buildozer --version
```

## 📱 Next Steps

1. **Customize Java Project**
   - Open in Android Studio
   - Modify MainActivity
   - Update app theme
   - Add features

2. **Enhance Kivy App**
   - Edit main.py
   - Add screens
   - Customize UI
   - Add dependencies

3. **Development Tips**
   - Use Android Studio for Java development
   - Use VS Code with Python extensions for Kivy
   - Test on real devices
   - Use virtual devices for testing

## 🔄 Updates and Maintenance

- Check Android SDK updates regularly
- Update Gradle when needed
- Keep Python packages updated
- Monitor deprecated APIs

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

- Create an issue for bugs
- Submit feature requests
- Check documentation for common solutions
- Join our community discussions
