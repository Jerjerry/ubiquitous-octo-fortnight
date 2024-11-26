import os
import subprocess
import platform
import sys
import zipfile
import shutil
import requests

def run_command(command):
    """Run a shell command and check for errors."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while executing: {command}\n{e}")
        exit(1)

def check_java():
    """Check if Java is installed and set JAVA_HOME."""
    print("Checking Java installation...")
    
    try:
        # Try to run java -version
        result = subprocess.run("java -version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("Java is already installed!")
            return True
    except:
        pass

    print("Java not found. Installing OpenJDK...")
    
    if platform.system() == "Windows":
        # Download OpenJDK for Windows
        print("Downloading OpenJDK...")
        jdk_url = "https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_windows-x64_bin.zip"
        run_command(f"curl -L -o jdk.zip {jdk_url}")
        
        # Extract JDK
        print("Extracting JDK...")
        run_command(f"powershell -Command \"Expand-Archive -Path jdk.zip -DestinationPath ./jdk -Force\"")
        
        # Set JAVA_HOME
        jdk_path = os.path.abspath("./jdk/jdk-17.0.2")
        os.environ["JAVA_HOME"] = jdk_path
        os.environ["PATH"] = f"{jdk_path}\\bin;{os.environ['PATH']}"
        
        print(f"Java installed and JAVA_HOME set to: {jdk_path}")
        return True
    else:
        print("Please install Java manually on non-Windows systems.")
        return False

def download_android_tools():
    """Download Android SDK command-line tools."""
    print("Downloading Android command-line tools...")
    if platform.system() == "Windows":
        url = "https://dl.google.com/android/repository/commandlinetools-win-9477386_latest.zip"
        filename = "commandlinetools.zip"
    elif platform.system() == "Darwin":
        url = "https://dl.google.com/android/repository/commandlinetools-mac-9477386_latest.zip"
        filename = "commandlinetools.zip"
    else:
        url = "https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip"
        filename = "commandlinetools.zip"

    run_command(f"curl -o {filename} {url}")
    print(f"Downloaded {filename}")
    return filename

def extract_tools(filename):
    """Extract Android command line tools to the correct directory structure."""
    print("Extracting Android command line tools...")
    
    # Create the required directory structure
    cmdline_tools_dir = os.path.join("android-sdk", "cmdline-tools")
    tools_latest_dir = os.path.join(cmdline_tools_dir, "latest")
    
    # Create directories if they don't exist
    os.makedirs(cmdline_tools_dir, exist_ok=True)
    
    # Extract to a temporary directory first
    temp_dir = "temp_tools"
    os.makedirs(temp_dir, exist_ok=True)
    
    if platform.system() == "Windows":
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    else:
        subprocess.run(["unzip", "-q", filename, "-d", temp_dir], check=True)
    
    # Move the contents to the correct location
    extracted_tools_dir = os.path.join(temp_dir, "cmdline-tools")
    if os.path.exists(tools_latest_dir):
        shutil.rmtree(tools_latest_dir)
    shutil.move(extracted_tools_dir, tools_latest_dir)
    
    # Cleanup
    shutil.rmtree(temp_dir)
    os.remove(filename)
    
    print("Android command line tools extracted successfully")

def accept_licenses():
    """Accept all Android SDK licenses."""
    print("Accepting Android SDK licenses...")
    
    # Create licenses directory if it doesn't exist
    licenses_dir = "./android-sdk/licenses"
    os.makedirs(licenses_dir, exist_ok=True)
    
    # Write license files directly
    license_files = {
        "android-sdk-license": "24333f8a63b6825ea9c5514f83c2829b004d1fee",
        "android-sdk-preview-license": "84831b9409646a918e30573bab4c9c91346d8abd",
        "intel-android-extra-license": "d975f751698a77b662f1254ddbeed3901e976f5a"
    }
    
    for license_name, license_key in license_files.items():
        with open(os.path.join(licenses_dir, license_name), 'w') as f:
            f.write("\n" + license_key + "\n")
    
    print("SDK licenses accepted.")

def install_sdk_and_ndk():
    """Install Android SDK components using sdkmanager."""
    print("Installing Android SDK components...")
    
    # Set up environment variables
    env = os.environ.copy()
    sdk_root = os.path.abspath("android-sdk")
    env["ANDROID_HOME"] = sdk_root
    env["ANDROID_SDK_ROOT"] = sdk_root
    
    # Construct the sdkmanager path
    if platform.system() == "Windows":
        sdkmanager = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "sdkmanager.bat")
    else:
        sdkmanager = os.path.join(sdk_root, "cmdline-tools", "latest", "bin", "sdkmanager")
        # Make sdkmanager executable on Unix systems
        os.chmod(sdkmanager, 0o755)
    
    # Accept licenses first (automatically)
    print("Accepting Android SDK licenses...")
    if platform.system() == "Windows":
        subprocess.run(f'echo y | "{sdkmanager}" --licenses', shell=True, env=env)
        # Additional Windows-specific license acceptance
        licenses = [
            "android-sdk-license",
            "android-sdk-preview-license",
            "android-sdk-arm-dbt-license",
            "google-gdk-license",
            "intel-android-extra-license",
            "mips-android-sysimage-license"
        ]
        licenses_dir = os.path.join(sdk_root, "licenses")
        os.makedirs(licenses_dir, exist_ok=True)
        for license_name in licenses:
            with open(os.path.join(licenses_dir, license_name), 'w') as f:
                f.write("\n8933bad161af4178b1185d1a37fbf41ea5269c55\n")
                f.write("\nd56f5187479451eabf01fb78af6dfcb131a6481e\n")
    else:
        subprocess.run(f'yes | "{sdkmanager}" --licenses', shell=True, env=env)
    
    # Install components one by one with proper error handling
    components = [
        "platform-tools",
        "platforms;android-31",
        "build-tools;31.0.0",
        "ndk;25.2.9519653"
    ]
    
    for component in components:
        print(f"\nInstalling {component}...")
        try:
            # Use yes command to automatically accept any prompts
            if platform.system() == "Windows":
                cmd = f'echo y | "{sdkmanager}" "{component}"'
            else:
                cmd = f'yes | "{sdkmanager}" "{component}"'
            subprocess.run(cmd, shell=True, env=env, check=True)
            print(f"Successfully installed {component}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {component}: {e}")
            print("Continuing with remaining components...")
            continue

    print("\nAndroid SDK components installation completed")

def download_file(url, filename):
    """Download a file from URL with progress indication."""
    try:
        print(f"Downloading from {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        
        with open(filename, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        if os.path.exists(filename):
            os.remove(filename)
        return False

def download_gradle():
    """Download and install Gradle."""
    print("Downloading Gradle...")
    gradle_version = "8.4"
    url = f"https://services.gradle.org/distributions/gradle-{gradle_version}-bin.zip"
    filename = os.path.abspath("gradle.zip")
    
    # First ensure any old files are cleaned up
    if os.path.exists(filename):
        os.remove(filename)
    
    # Download Gradle using the new download function
    if not download_file(url, filename):
        print("Failed to download Gradle. Please check your internet connection and try again.")
        return False
    
    # Verify the zip file
    try:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            # Create gradle directory if it doesn't exist
            gradle_dir = os.path.abspath("gradle")
            os.makedirs(gradle_dir, exist_ok=True)
            
            print("Extracting Gradle...")
            zip_ref.extractall(gradle_dir)
    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid zip file.")
        if os.path.exists(filename):
            os.remove(filename)
        return False
    except Exception as e:
        print(f"Error extracting Gradle: {e}")
        if os.path.exists(filename):
            os.remove(filename)
        return False
    
    try:
        # Set up environment variables
        gradle_home = os.path.join(gradle_dir, f"gradle-{gradle_version}")
        os.environ["GRADLE_HOME"] = gradle_home
        
        # Add Gradle to PATH
        gradle_bin = os.path.join(gradle_home, "bin")
        if platform.system() == "Windows":
            os.environ["PATH"] = f"{gradle_bin};{os.environ['PATH']}"
        else:
            os.environ["PATH"] = f"{gradle_bin}:{os.environ['PATH']}"
        
        # Clean up
        os.remove(filename)
        print(f"Gradle {gradle_version} installed successfully")
        print(f"GRADLE_HOME set to: {gradle_home}")
        
        # Verify gradle installation
        gradle_exe = "gradle.bat" if platform.system() == "Windows" else "gradle"
        gradle_path = os.path.join(gradle_bin, gradle_exe)
        
        if os.path.exists(gradle_path):
            print("Gradle installation verified successfully")
            return True
        else:
            print(f"Warning: Gradle executable not found at {gradle_path}")
            return False
            
    except Exception as e:
        print(f"Error setting up Gradle environment: {e}")
        return False

def create_android_project_template(app_name, package_name):
    """Create a basic Android project template."""
    print(f"Creating Android project: {app_name}")
    
    # Create project directory
    os.makedirs(app_name, exist_ok=True)
    os.chdir(app_name)
    
    # Create project structure
    directories = [
        "app/src/main/java/" + package_name.replace(".", "/"),
        "app/src/main/res/layout",
        "app/src/main/res/values",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create build.gradle (Project level)
    with open("build.gradle", "w") as f:
        f.write("""buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.0.4'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}""")
    
    # Create settings.gradle
    with open("settings.gradle", "w") as f:
        f.write(f"""include ':app'
rootProject.name = "{app_name}"
""")
    
    # Create app/build.gradle
    with open("app/build.gradle", "w") as f:
        f.write(f"""plugins {{
    id 'com.android.application'
}}

android {{
    compileSdkVersion 31
    
    defaultConfig {{
        applicationId "{package_name}"
        minSdkVersion 21
        targetSdkVersion 31
        versionCode 1
        versionName "1.0"
    }}
    
    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
    
    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.4.1'
    implementation 'com.google.android.material:material:1.5.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.3'
}}""")
    
    # Create AndroidManifest.xml
    manifest_path = "app/src/main/AndroidManifest.xml"
    with open(manifest_path, "w") as f:
        f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>""")
    
    # Create MainActivity.java
    main_activity_path = f"app/src/main/java/{package_name.replace('.', '/')}/MainActivity.java"
    with open(main_activity_path, "w") as f:
        f.write(f"""package {package_name};

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }}
}}""")
    
    # Create activity_main.xml
    with open("app/src/main/res/layout/activity_main.xml", "w") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>""")
    
    # Create strings.xml
    with open("app/src/main/res/values/strings.xml", "w") as f:
        f.write(f"""<resources>
    <string name="app_name">{app_name}</string>
</resources>""")
    
    # Initialize Gradle wrapper
    gradle_path = os.path.join(os.environ.get("GRADLE_HOME", ""), "bin", "gradle")
    if platform.system() == "Windows":
        gradle_path += ".bat"
    
    try:
        subprocess.run([gradle_path, "wrapper"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error initializing Gradle wrapper: {e}")
        print("Continuing with project creation...")
    except FileNotFoundError:
        print("Gradle not found in PATH. Attempting to use gradlew directly...")
        try:
            # Try to download gradle-wrapper.jar and gradle-wrapper.properties directly
            wrapper_url = "https://raw.githubusercontent.com/gradle/gradle/v8.4.0/gradle/wrapper/gradle-wrapper.jar"
            properties_url = "https://raw.githubusercontent.com/gradle/gradle/v8.4.0/gradle/wrapper/gradle-wrapper.properties"
            
            os.makedirs("gradle/wrapper", exist_ok=True)
            
            # Download wrapper JAR
            run_command(f'curl -o "gradle/wrapper/gradle-wrapper.jar" {wrapper_url}')
            
            # Download wrapper properties
            run_command(f'curl -o "gradle/wrapper/gradle-wrapper.properties" {properties_url}')
            
            # Create gradlew and gradlew.bat
            with open("gradlew", "w") as f:
                f.write("""#!/usr/bin/env sh
exec java -jar gradle/wrapper/gradle-wrapper.jar "$@"
""")
            
            with open("gradlew.bat", "w") as f:
                f.write("""@echo off
java -jar gradle\\wrapper\\gradle-wrapper.jar %*
""")
            
            # Make gradlew executable
            if platform.system() != "Windows":
                os.chmod("gradlew", 0o755)
        except Exception as e:
            print(f"Error setting up Gradle wrapper manually: {e}")
    
    os.chdir("..")
    print(f"Android project '{app_name}' created successfully!")

def install_python_dependencies():
    """Install required Python packages."""
    print("Installing Python dependencies...")
    packages = [
        "buildozer",
        "kivy",
        "cython"
    ]
    for package in packages:
        print(f"Installing {package}...")
        run_command(f"pip install {package}")

def create_kivy_project_template(app_name):
    """Create a basic Kivy project template."""
    print(f"Creating Kivy project: {app_name}")
    
    # Create project directory
    project_dir = f"./{app_name}"
    os.makedirs(project_dir, exist_ok=True)
    
    # Create main.py
    with open(f"{project_dir}/main.py", "w") as f:
        f.write("""from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Create a label
        label = Label(
            text='Welcome to Your First Kivy App!',
            size_hint=(1, 0.5),
            font_size='24sp'
        )
        
        # Create a button
        button = Button(
            text='Click Me!',
            size_hint=(1, 0.5),
            font_size='20sp'
        )
        button.bind(on_press=self.on_button_press)
        
        # Add widgets to layout
        layout.add_widget(label)
        layout.add_widget(button)
        
        return layout
    
    def on_button_press(self, instance):
        instance.text = 'Button Pressed!'

if __name__ == '__main__':
    MainApp().run()
""")
    
    # Create buildozer.spec
    with open(f"{project_dir}/buildozer.spec", "w") as f:
        f.write(f"""[app]
title = {app_name}
package.name = {app_name.lower()}
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25.2.9519653
android.private_storage = True
android.accept_sdk_license = True
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
""")
    
    print(f"Kivy project '{app_name}' created successfully!")
    print("\nTo build the Android APK:")
    print(f"1. cd {app_name}")
    print("2. buildozer init")
    print("3. buildozer android debug")
    print("\nThe APK will be in the bin/ directory")

def verify_installation():
    """Verify that SDK and NDK components are installed."""
    sdk_path = "./android-sdk" if platform.system() != "Windows" else ".\\android-sdk"
    required_dirs = [
        f"{sdk_path}/platform-tools",
        f"{sdk_path}/platforms/android-31",
        f"{sdk_path}/build-tools/31.0.0",
        f"{sdk_path}/ndk/25.2.9519653"
    ]
    
    print("Verifying installation...")
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"Missing: {directory}")
            exit(1)
    print("All required components are installed successfully!")

def main():
    """Main function to set up the Android development environment."""
    print("Starting Android development environment setup...")
    
    # Install dependencies in order
    if not download_gradle():
        print("Error: Failed to install Gradle. Please check the logs above for details.")
        return
    
    # Create directories
    os.makedirs("android-sdk", exist_ok=True)
    
    # Install Java if needed
    if not check_java():
        print("Java installation required. Please install Java and try again.")
        exit(1)
    
    tools_filename = download_android_tools()
    extract_tools(tools_filename)
    install_sdk_and_ndk()
    install_python_dependencies()
    verify_installation()
    create_android_project_template("MyJavaApp", "com.example.myjavaapp")
    create_kivy_project_template("MyKivyApp")
    
    print("\nAndroid development environment setup complete!")
    print("\nTwo sample projects have been created:")
    print("\n1. Java-based Android app (MyJavaApp):")
    print("   - Open in Android Studio")
    print("   - Build: './gradlew build'")
    print("   - Run: './gradlew installDebug'")
    print("\n2. Python-based Kivy app (MyKivyApp):")
    print("   - cd MyKivyApp")
    print("   - buildozer init")
    print("   - buildozer android debug")
    print("   - APK will be in the bin/ directory")

if __name__ == "__main__":
    main()
