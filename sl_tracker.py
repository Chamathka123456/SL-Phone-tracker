#!/usr/bin/env python3
"""
🇱🇰 Sri Lankan Phone Tracker with Real Geolocation
Shows exact addresses, coordinates, and Google Maps links
For Educational Purposes Only
"""

import sys
import os
import webbrowser
import json
import requests
from datetime import datetime

def check_dependencies():
    """Install required packages"""
    packages = ['phonenumbers', 'folium', 'opencage']
    missing = []
    
    for package in packages:
        try:
            if package == 'opencage':
                from opencage.geocoder import OpenCageGeocode
            elif package == 'folium':
                import folium
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"📦 Installing missing packages: {', '.join(missing)}")
        for package in missing:
            os.system(f"pip install {package} --user")
        print("✅ Packages installed!")

def get_opencage_key():
    """Get or request OpenCage API key"""
    key_file = "api_key.txt"
    
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            return f.read().strip()
    
    print("\n" + "="*60)
    print("🔑 OPEN CAGE API KEY REQUIRED FOR REAL LOCATIONS")
    print("="*60)
    print("1. Visit: https://opencagedata.com/api")
    print("2. Sign up for FREE account (2500 requests/day)")
    print("3. Get your API key")
    print("4. Enter it below")
    print("-"*60)
    
    api_key = input("Enter your OpenCage API key: ").strip()
    
    if api_key:
        with open(key_file, 'w') as f:
            f.write(api_key)
        print("✅ API key saved to api_key.txt")
        return api_key
    else:
        print("⚠️  Using limited functionality (no precise locations)")
        return None

def get_phone_info(phone):
    """Get basic phone information"""
    try:
        from phonenumbers import parse, format_number, PhoneNumberFormat
        from phonenumbers import carrier, timezone, geocoder
        
        # Format number
        original = phone
        if phone.startswith('0'):
            phone = '+94' + phone[1:]
        elif phone.startswith('94'):
            phone = '+' + phone
        
        parsed = parse(phone, "LK")
        
        # Sri Lankan operators
        operators = {
            '70': 'Mobitel', '71': 'Mobitel', '81': 'Mobitel',
            '72': 'Dialog', '74': 'Dialog', '76': 'Dialog',
            '75': 'Airtel',
            '77': 'Hutch', '78': 'Hutch'
        }
        
        # Get basic info
        digits = phone.replace('+', '')
        prefix = digits[4:6] if digits.startswith('94') else "Unknown"
        operator = operators.get(prefix, carrier.name_for_number(parsed, 'en') or "Unknown")
        
        info = {
            'original': original,
            'international': format_number(parsed, PhoneNumberFormat.INTERNATIONAL),
            'national': format_number(parsed, PhoneNumberFormat.NATIONAL),
            'operator': operator,
            'country': geocoder.description_for_number(parsed, 'en'),
            'timezone': timezone.time_zones_for_number(parsed)[0] if timezone.time_zones_for_number(parsed) else "Asia/Colombo",
            'prefix': prefix
        }
        
        return True, info
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_real_location(api_key, location_name):
    """Get real coordinates and address using OpenCage"""
    try:
        from opencage.geocoder import OpenCageGeocode
        
        geocoder = OpenCageGeocode(api_key)
        
        # Add Sri Lanka for better accuracy
        query = f"{location_name}, Sri Lanka"
        results = geocoder.geocode(query)
        
        if results and len(results) > 0:
            result = results[0]
            return {
                'formatted': result['formatted'],
                'latitude': result['geometry']['lat'],
                'longitude': result['geometry']['lng'],
                'components': result.get('components', {}),
                'confidence': result.get('confidence', 0)
            }
    except Exception as e:
        print(f"⚠️  Location API error: {e}")
    
    return None

def create_interactive_map(lat, lng, phone_info, location_data):
    """Create interactive map with Folium"""
    import folium
    
    # Create map centered on location
    phone_map = folium.Map(location=[lat, lng], zoom_start=12)
    
    # Add marker with popup
    popup_html = f"""
    <div style="font-family: Arial; width: 250px;">
        <h3 style="color: #d35400;">📱 Phone Information</h3>
        <b>Number:</b> {phone_info['international']}<br>
        <b>Operator:</b> {phone_info['operator']}<br>
        <b>Prefix:</b> {phone_info['prefix']}<br>
        <b>Country:</b> {phone_info['country']}<br>
        <b>Timezone:</b> {phone_info['timezone']}<br>
        <hr>
        <b>📍 Exact Location:</b><br>
        {location_data['formatted']}<br>
        <b>Coordinates:</b> {lat:.6f}, {lng:.6f}<br>
        <b>Confidence:</b> {location_data.get('confidence', 'N/A')}%
    </div>
    """
    
    folium.Marker(
        [lat, lng],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"📱 {phone_info['national']}",
        icon=folium.Icon(color='red', icon='phone', prefix='fa')
    ).add_to(phone_map)
    
    # Add circle for approximate area
    folium.Circle(
        location=[lat, lng],
        radius=2000,
        color='blue',
        fill=True,
        fill_opacity=0.2,
        tooltip="Approximate coverage area"
    ).add_to(phone_map)
    
    # Save map
    filename = f"map_{phone_info['international'].replace('+', '').replace(' ', '_')}.html"
    phone_map.save(filename)
    
    return filename

def generate_google_maps_link(lat, lng):
    """Generate Google Maps and OpenStreetMap links"""
    google_url = f"https://www.google.com/maps?q={lat},{lng}&z=15"
    osm_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=15/{lat}/{lng}"
    
    return google_url, osm_url

def print_banner():
    """Display banner"""
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║   🇱🇰 SRI LANKAN PHONE TRACKER - ADVANCED EDITION   ║
    ║         With Real Geolocation & Maps                ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main program"""
    print_banner()
    
    # Check dependencies
    check_dependencies()
    
    # Get API key
    api_key = get_opencage_key()
    
    print("\n📞 Supported Formats:")
    print("   • +94701234567  • 94701234567  • 0701234567")
    print("\n📡 Sri Lankan Operators:")
    print("   • Mobitel: 70, 71, 81  • Dialog: 72, 74, 76")
    print("   • Airtel: 75           • Hutch: 77, 78")
    print("="*60)
    
    while True:
        try:
            print("\n" + "─"*40)
            phone = input("Enter Sri Lankan phone number (or 'quit'): ").strip()
            
            if phone.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using the tracker!")
                break
            
            if not phone:
                continue
            
            print(f"\n🔍 Analyzing: {phone}")
            print("─"*40)
            
            # Get basic phone info
            success, result = get_phone_info(phone)
            
            if not success:
                print(f"❌ {result}")
                continue
            
            print("\n📱 BASIC INFORMATION:")
            print(f"   📞 Number: {result['international']}")
            print(f"   📱 National: {result['national']}")
            print(f"   📡 Operator: {result['operator']} (Prefix: {result['prefix']})")
            print(f"   🇱🇰 Country: {result['country']}")
            print(f"   🕐 Timezone: {result['timezone']}")
            
            # Get real location if API key available
            if api_key:
                print("\n📍 GETTING REAL LOCATION...")
                location_data = get_real_location(api_key, result['country'])
                
                if location_data:
                    print("\n✅ EXACT LOCATION FOUND:")
                    print(f"   🏠 Address: {location_data['formatted']}")
                    print(f"   📍 Coordinates: {location_data['latitude']:.6f}, {location_data['longitude']:.6f}")
                    
                    # Extract location components
                    components = location_data.get('components', {})
                    if 'city' in components:
                        print(f"   🏙️  City: {components['city']}")
                    if 'state' in components:
                        print(f"   🏛️  State: {components['state']}")
                    if 'postcode' in components:
                        print(f"   📮 Postal Code: {components['postcode']}")
                    
                    # Generate map links
                    google_url, osm_url = generate_google_maps_link(
                        location_data['latitude'], 
                        location_data['longitude']
                    )
                    
                    print(f"\n🌐 MAP LINKS:")
                    print(f"   • Google Maps: {google_url}")
                    print(f"   • OpenStreetMap: {osm_url}")
                    
                    # Create interactive map
                    try:
                        print("\n🗺️  CREATING INTERACTIVE MAP...")
                        map_file = create_interactive_map(
                            location_data['latitude'],
                            location_data['longitude'],
                            result,
                            location_data
                        )
                        print(f"   ✅ Map saved: {map_file}")
                        
                        # Ask to open
                        open_map = input("\nOpen map in browser? (y/n): ").lower()
                        if open_map == 'y':
                            webbrowser.open(f'file://{os.path.abspath(map_file)}')
                            print("   🌐 Opening map...")
                    
                    except Exception as e:
                        print(f"   ⚠️  Map creation failed: {e}")
                
                else:
                    print("❌ Could not find exact location")
                    print("💡 Tip: The number might be registered to a general area")
            
            else:
                print("\n⚠️  Enable full features with OpenCage API key:")
                print("   Visit: https://opencagedata.com/api")
            
            # Save results to file
            save_result = input("\n💾 Save results to file? (y/n): ").lower()
            if save_result == 'y':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"result_{result['international'].replace('+', '').replace(' ', '_')}_{timestamp}.txt"
                
                with open(filename, 'w') as f:
                    f.write("="*60 + "\n")
                    f.write("SRI LANKAN PHONE TRACKER RESULTS\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"Phone Number: {result['international']}\n")
                    f.write(f"National Format: {result['national']}\n")
                    f.write(f"Operator: {result['operator']}\n")
                    f.write(f"Country: {result['country']}\n")
                    f.write(f"Timezone: {result['timezone']}\n")
                    
                    if api_key and location_data:
                        f.write("\n" + "-"*60 + "\n")
                        f.write("EXACT LOCATION:\n")
                        f.write(f"Address: {location_data['formatted']}\n")
                        f.write(f"Coordinates: {location_data['latitude']}, {location_data['longitude']}\n")
                
                print(f"✅ Results saved to: {filename}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Program terminated")
            break
        except Exception as e:
            print(f"\n⚠️  Error: {e}")

if __name__ == "__main__":
    main()
