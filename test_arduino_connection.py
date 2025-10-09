#!/usr/bin/env python3
"""
Test script to verify Arduino connection and troubleshoot serial issues.
Run this script to test your Arduino connection before running the Flask app.
"""

import sys
import time
from arduino import ArduinoConnection

def test_arduino_connection():
    """Test Arduino connection with detailed error reporting."""
    print("🔍 Testing Arduino Connection...")
    print("=" * 50)
    
    # Test 1: List available ports
    print("\n1. Scanning for available serial ports...")
    try:
        temp_conn = ArduinoConnection.__new__(ArduinoConnection)  # Create without __init__
        ports = temp_conn.get_available_ports()
        if ports:
            print(f"✅ Found {len(ports)} port(s): {', '.join(ports)}")
        else:
            print("❌ No serial ports found!")
            print("   - Make sure your Arduino is connected")
            print("   - Check if drivers are installed")
            return False
    except Exception as e:
        print(f"❌ Error scanning ports: {e}")
        return False
    
    # Test 2: Try to connect to Arduino
    print("\n2. Attempting to connect to Arduino...")
    try:
        arduino = ArduinoConnection()  # Auto-detect port
        print(f"✅ Successfully connected to Arduino on {arduino.port}")
        
        # Test 3: Test basic communication
        print("\n3. Testing basic communication...")
        try:
            arduino.reset_buffers()
            print("✅ Buffer reset successful")
            
            # Send a test command (adjust based on your Arduino code)
            arduino.write(b'A')  # Request available pins
            print("✅ Command sent successfully")
            
            # Try to read response with timeout
            print("   Waiting for response...")
            time.sleep(1)  # Give Arduino time to respond
            
            if arduino.serial_connection.in_waiting:
                response = arduino.readline().decode(errors='ignore').strip()
                print(f"✅ Received response: {response}")
            else:
                print("⚠️ No response received (this might be normal if Arduino doesn't respond to 'A' command)")
                
        except Exception as e:
            print(f"❌ Communication test failed: {e}")
            return False
        
        # Test 4: Close connection
        print("\n4. Testing connection cleanup...")
        arduino.close()
        print("✅ Connection closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Arduino: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   - Make sure Arduino is connected via USB")
        print("   - Check if another program is using the serial port")
        print("   - Try unplugging and reconnecting the Arduino")
        print("   - Verify Arduino drivers are installed")
        print("   - Try running as administrator (Windows)")
        print("   - Check if Arduino IDE Serial Monitor is open (close it)")
        return False

def main():
    """Main test function."""
    print("Arduino Serial Connection Test")
    print("=" * 50)
    
    success = test_arduino_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your Arduino connection is working.")
        print("You can now run your Flask app: python app.py")
    else:
        print("❌ Connection test failed. Please fix the issues above.")
        print("\nAdditional help:")
        print("- Check Windows Device Manager for COM port conflicts")
        print("- Try different USB cables or ports")
        print("- Restart your computer if drivers seem corrupted")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
