#!/usr/bin/env python3
"""
🇱🇰 Sri Lankan Phone Tracker - Advanced Edition
Shows real locations, maps, and detailed information
For Educational Purposes Only
"""

import os
import sys
import webbrowser
import json
from datetime import datetime

# Try to import required packages
try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone, PhoneNumberFormat
    HAS_PHONENUMBERS = True
except ImportError:
    HAS_PHONENUMBERS = False

try:
    from opencage.geocoder import OpenCageGeocode
    HAS_OPENCAGE = True
except ImportError:
    HAS_OPENCAGE = False

try:
    import folium
    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False

# Sri Lankan database
SRI_LANKA_DB = {
    'prefix_locations': {
        '70': 'Colombo/Urban Areas',
        '71': 'Colombo/Western Province', 
        '72': 'Colombo/Metro Areas',
        '74': 'Colombo/Suburbs',
        '75': 'Urban Centers',
        '76': 'Major Cities',
        '77': 'Colombo & Suburbs',
        '78': 'Urban Areas',
        '81': 'Kandy/Central Province'
    },
    'operators': {
        '70': 'Mobitel', '71': 'Mobitel', '81': 'Mobitel',
        '72': 'Dialog', '74': 'Dialog', '76': 'Dialog', '77': 'Dialog',
        '75': 'Airtel', '78': 'Hutch'
    },
    'area_codes': {
        '011': 'Colombo City', '081': 'Kandy', '021': 'Jaffna',
        '031': 'Gampaha', '041': 'Matara', '051': 'Negombo',
        '036': 'Kalutara', '045': 'Ratnapura', '047': 'Kegalle'
    }
}

def install_dependencies():
    """Install missing packages"""
    print("\n🔧 Installing required packages...")
    
    if not HAS_PHONENUMBERS:
        print("Installing phonenumbers...")
        os.system(f"{sys.executable} -m pip install phonenumbers")
    
    if not HAS_OPENCAGE:
        print("Installing opencage...")
        os.system(f"{sys.executable} -m pip install opencage")
    
    if not HAS_FOLIUM:
        print("Installing folium...")
        os.system(f"{sys.executable} -m pip install folium")
    
    print("✅ Packages installed! Please restart the script.")
    sys.exit(0)

def get_api_key():
    """Get OpenCage API key"""
    key_file = "api_key.txt"
    
    if os.path.exists(key_file):
        with open(key_file, 'r') as f:
            key = f.read().strip()
            if key and key != "YOUR_API_KEY_HERE":
                return key
    
    print("\n" + "🔑" * 30)
    print("   OPEN CAGE API KEY REQUIRED")
    print("🔑" * 30)
    print("For EXACT locations and maps, you need an API key.")
    print("\n📋 How to get it (FREE):")
    print("1. Visit: https://opencagedata.com/api")
    print("2. Sign up for FREE account")
    print("3. Get API key (2500 requests/day free)")
    print("4. Enter it below or save in api_key.txt")
    print("-" * 50)
    
    key = input("Enter API key (or press Enter to skip): ").strip()
    
    if key:
        with open(key_file, 'w') as f:
            f.write(key)
        print("✅ API key saved!")
        return key
    
    return None

def analyze_number(phone):
    """Analyze Sri Lankan phone number"""
    try:
        # Format number
        original = phone
        clean = phone.replace(' ', '').replace('-', '').replace('+', '')
        
        if clean.startswith('0') and len(clean) == 10:
            formatted = '+94' + clean[1:]
        elif clean.startswith('94'):
            formatted = '+' + clean
        else:
            formatted = phone
        
        # Parse
        parsed = phonenumbers.parse(formatted, "LK")
        
        if not phonenumbers.is_valid_number(parsed):
            return None, "Invalid phone number"
        
        # Basic info
        national = phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL)
        international = phonenumbers.format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
        
        # Get operator
        op = carrier.name_for_number(parsed, 'en')
        if not op:
            prefix = formatted[3:5] if len(formatted) > 4 else '70'
            op = SRI_LANKA_DB['operators'].get(prefix, 'Unknown')
        
        # Get location from prefix
        prefix = formatted[3:5] if len(formatted) > 4 else '70'
        approx_location = SRI_LANKA_DB['prefix_locations'].get(prefix, 'Sri Lanka')
        
        # Timezone
        tz_list = timezone.time_zones_for_number(parsed)
        timezone_str = tz_list[0] if tz_list else "Asia/Colombo"
        
        # Number type
        num_type = phonenumbers.number_type(parsed)
        type_map = {0: "Fixed Line", 1: "Mobile", 3: "Toll Free", 9: "VoIP"}
        number_type = type_map.get(num_type, "Mobile")
        
        # Build result
        result = {
            'original': original,
            'clean': clean,
            'national': national,
            'international': international,
            'operator': op,
            'prefix': prefix,
            'approx_location': approx_location,
            'country': geocoder.description_for_number(parsed, 'en'),
            'timezone': timezone_str,
            'type': number_type,
            'valid': True
        }
        
        return result, "Success"
        
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_exact_location(api_key, location_name):
    """Get exact coordinates and address"""
    try:
        geocoder = OpenCageGeocode(api_key)
        query = f"{location_name}, Sri Lanka"
        results = geocoder.geocode(query)
        
        if results:
            result = results[0]
            return {
                'address': result['formatted'],
                'latitude': result['geometry']['lat'],
                'longitude': result['geometry']['lng'],
                'components': result.get('components', {}),
                'confidence': result.get('confidence', 0)
            }
    except:
        pass
    
    return None

def create_map(phone_info, location_data):
    """Create interactive map"""
    try:
        # Create map
        m = folium.Map(
            location=[location_data['latitude'], location_data['longitude']],
            zoom_start=13
        )
        
        # Popup HTML
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="color: #e74c3c;">📱 Phone Information</h4>
            <b>Number:</b> {phone_info['national']}<br>
            <b>Operator:</b> {phone_info['operator']}<br>
            <b>Type:</b> {phone_info['type']}<br>
            <hr>
            <b>📍 Location:</b><br>
            {location_data['address']}<br>
            <b>📌 Coordinates:</b><br>
            {location_data['latitude']:.6f}, {location_data['longitude']:.6f}
        </div>
        """
        
        # Add marker
        folium.Marker(
            [location_data['latitude'], location_data['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"📞 {phone_info['national']}",
            icon=folium.Icon(color='red', icon='phone', prefix='fa')
        ).add_to(m)
        
        # Add circle
        folium.Circle(
            location=[location_data['latitude'], location_data['longitude']],
            radius=1000,
            color='blue',
            fill=True,
            fill_opacity=0.2
        ).add_to(m)
        
        # Save
        filename = f"map_{phone_info['clean']}.html"
        m.save(filename)
        
        return filename
    except:
        return None

def display_results(phone_info, exact_location=None):
    """Display all results"""
    print("\n" + "═" * 60)
    print("📱 SRI LANKAN PHONE TRACKER RESULTS")
    print("═" * 60)
    
    print(f"📞 Original Input: {phone_info['original']}")
    print(f"🇱🇰 National Format: {phone_info['national']}")
    print(f"🌍 International: {phone_info['international']}")
    print(f"📡 Operator: {phone_info['operator']}")
    print(f"🔢 Prefix: {phone_info['prefix']}")
    print(f"📍 Approximate Area: {phone_info['approx_location']}")
    print(f"🏷️ Type: {phone_info['type']}")
    print(f"🕐 Timezone: {phone_info['timezone']}")
    print(f"🇱🇰 Country: {phone_info['country']}")
    
    if exact_location:
        print("\n" + "📍" * 30)
        print("   EXACT LOCATION FOUND!")
        print("📍" * 30)
        print(f"🏠 Address: {exact_location['address']}")
        print(f"📌 Coordinates: {exact_location['latitude']:.6f}, {exact_location['longitude']:.6f}")
        
        # Show components
        comp = exact_location['components']
        if 'city' in comp:
            print(f"🏙️ City: {comp['city']}")
        if 'state_district' in comp:
            print(f"🗺️ District: {comp['state_district']}")
        if 'postcode' in comp:
            print(f"📮 Postal Code: {comp['postcode']}")
        
        # Google Maps link
        print(f"\n🗺️ Google Maps: https://maps.google.com/?q={exact_location['latitude']},{exact_location['longitude']}")
    
    print("═" * 60)

def save_report(phone_info, exact_location=None):
    """Save report to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{phone_info['clean']}_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write("="*60 + "\n")
        f.write("SRI LANKAN PHONE TRACKER - DETAILED REPORT\n")
        f.write("="*60 + "\n\n")
        
        f.write("📱 BASIC INFORMATION:\n")
        f.write("-"*40 + "\n")
        f.write(f"Original Input: {phone_info['original']}\n")
        f.write(f"National Format: {phone_info['national']}\n")
        f.write(f"International: {phone_info['international']}\n")
        f.write(f"Operator: {phone_info['operator']}\n")
        f.write(f"Prefix: {phone_info['prefix']}\n")
        f.write(f"Approximate Area: {phone_info['approx_location']}\n")
        f.write(f"Type: {phone_info['type']}\n")
        f.write(f"Timezone: {phone_info['timezone']}\n")
        f.write(f"Country: {phone_info['country']}\n\n")
        
        if exact_location:
            f.write("📍 EXACT LOCATION:\n")
            f.write("-"*40 + "\n")
            f.write(f"Address: {exact_location['address']}\n")
            f.write(f"Coordinates: {exact_location['latitude']}, {exact_location['longitude']}\n")
            f.write(f"Google Maps: https://maps.google.com/?q={exact_location['latitude']},{exact_location['longitude']}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("Report generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("="*60 + "\n")
    
    return filename

def main():
    """Main program"""
    # Banner
    print("\n" + "🇱🇰" * 25)
    print("   SRI LANKAN PHONE TRACKER - ADVANCED EDITION")
    print("        With Real Locations & Maps")
    print("🇱🇰" * 25)
    
    # Check dependencies
    if not HAS_PHONENUMBERS or not HAS_OPENCAGE or not HAS_FOLIUM:
        install_dependencies()
    
    # Get API key
    api_key = get_api_key()
    
    print("\n📞 Enter numbers in these formats:")
    print("   • 0770851207    • +94770851207")
    print("   • 0701234567    • 0112345678 (landline)")
    print("\n📡 Common Prefixes:")
    print("   70-72,74: Colombo Area")
    print("   77,78: Dialog/Hutch")
    print("   81: Kandy Area")
    print("=" * 60)
    
    while True:
        try:
            print("\n" + "-" * 40)
            phone = input("\nEnter phone number (or 'quit'): ").strip()
            
            if phone.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Sri Lankan Phone Tracker!")
                break
            
            if not phone:
                continue
            
            print(f"\n🔍 Analyzing: {phone}")
            print("-" * 40)
            
            # Analyze number
            phone_info, status = analyze_number(phone)
            
            if not phone_info:
                print(f"❌ {status}")
                continue
            
            # Get exact location if API key available
            exact_location = None
            if api_key:
                print("📍 Getting exact location...")
                exact_location = get_exact_location(api_key, phone_info['country'])
            
            # Display results
            display_results(phone_info, exact_location)
            
            # Create map if location available
            if exact_location and HAS_FOLIUM:
                map_file = create_map(phone_info, exact_location)
                if map_file:
                    print(f"\n🗺️ Interactive map created: {map_file}")
                    open_map = input("Open map in browser? (y/n): ").lower()
                    if open_map == 'y':
                        webbrowser.open(f'file://{os.path.abspath(map_file)}')
            
            # Save report
            save_option = input("\n💾 Save detailed report? (y/n): ").lower()
            if save_option == 'y':
                report_file = save_report(phone_info, exact_location)
                print(f"✅ Report saved: {report_file}")
            
            # Tips
            print("\n💡 TIPS:")
            print(f"• Prefix {phone_info['prefix']} = {phone_info['approx_location']}")
            print(f"• {phone_info['operator']} is best in {phone_info['approx_location']}")
            if not api_key:
                print("• Get API key for exact addresses: https://opencagedata.com/api")
            
        except KeyboardInterrupt:
            print("\n\n👋 Program terminated by user")
            break
        except Exception as e:
            print(f"\n⚠️ Error: {e}")

if __name__ == "__main__":
    main()
