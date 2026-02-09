#!/usr/bin/env python3
"""
🇱🇰 Sri Lankan Phone Number Tracker
For Educational Purposes Only
"""

import sys
import os

def check_install():
    """Check and install phonenumbers library"""
    try:
        import phonenumbers
        print("✅ Required packages already installed")
    except ImportError:
        print("📦 Installing required package: phonenumbers")
        os.system("pip3 install phonenumbers --user")
        print("✅ Installation complete!")
        
        # Try importing again
        try:
            import phonenumbers
        except ImportError:
            print("❌ Installation failed. Please install manually:")
            print("   pip3 install phonenumbers")
            sys.exit(1)

def get_phone_info(phone):
    """Get information about Sri Lankan phone number"""
    try:
        from phonenumbers import parse, is_valid_number, format_number
        from phonenumbers import carrier, timezone, geocoder
        from phonenumbers import PhoneNumberFormat
        
        # Sri Lankan operator database
        operators = {
            '70': 'SLT-Mobitel', '71': 'SLT-Mobitel',
            '72': 'Dialog', '74': 'Dialog', '76': 'Dialog',
            '75': 'Airtel',
            '77': 'Hutch', '78': 'Hutch',
            '81': 'SLT-Mobitel'
        }
        
        # Format the number
        original = phone
        if phone.startswith('0') and len(phone) == 10:
            phone = '+94' + phone[1:]
        elif phone.startswith('94') and len(phone) == 11:
            phone = '+' + phone
        elif not phone.startswith('+94'):
            phone = '+94' + phone.lstrip('0')
        
        # Parse the number
        parsed = parse(phone, "LK")
        
        if not is_valid_number(parsed):
            return None, f"Invalid Sri Lankan number: {original}"
        
        # Get basic info
        national = format_number(parsed, PhoneNumberFormat.NATIONAL)
        international = format_number(parsed, PhoneNumberFormat.INTERNATIONAL)
        
        # Get operator
        op = carrier.name_for_number(parsed, "en")
        if not op:
            digits = phone.replace('+', '')
            if digits.startswith('94'):
                prefix = digits[4:6]
                op = operators.get(prefix, "Unknown Operator")
        
        # Get location and timezone
        location = geocoder.description_for_number(parsed, "en")
        tz_list = timezone.time_zones_for_number(parsed)
        timezone_str = tz_list[0] if tz_list else "Asia/Colombo"
        
        # Prepare result
        result = {
            'original': original,
            'national': national,
            'international': international,
            'operator': op,
            'location': location,
            'timezone': timezone_str,
            'country': 'Sri Lanka',
            'country_code': '94'
        }
        
        return result, "Success"
        
    except Exception as e:
        return None, f"Error processing number: {str(e)}"

def print_banner():
    """Display banner"""
    banner = """
    ╔══════════════════════════════════════════╗
    ║    🇱🇰 SRI LANKAN PHONE TRACKER 🇱🇰     ║
    ║        EDUCATIONAL USE ONLY             ║
    ╚══════════════════════════════════════════╝
    """
    print(banner)

def print_info(info):
    """Display phone information"""
    print("\n" + "═" * 50)
    print("📱 PHONE NUMBER INFORMATION")
    print("═" * 50)
    print(f"📞 Original Input: {info['original']}")
    print(f"🇱🇰 National Format: {info['national']}")
    print(f"🌍 International: {info['international']}")
    print(f"📡 Operator: {info['operator']}")
    print(f"📍 Location: {info['location']}")
    print(f"🕐 Timezone: {info['timezone']}")
    print(f"🇱🇰 Country: {info['country']} (+{info['country_code']})")
    print("═" * 50)

def main():
    """Main program"""
    print_banner()
    
    # Check and install dependencies
    check_install()
    
    print("📞 Accepted Formats:")
    print("   • +94701234567")
    print("   • 94701234567")
    print("   • 0701234567")
    print("   • 070-123-4567")
    print("\n📡 Operator Codes:")
    print("   • 70,71,81 - Mobitel")
    print("   • 72,74,76 - Dialog")
    print("   • 75 - Airtel")
    print("   • 77,78 - Hutch")
    print("─" * 50)
    
    while True:
        try:
            print("\n" + "─" * 30)
            phone_input = input("Enter phone number (or 'quit'): ").strip()
            
            if phone_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using Sri Lankan Phone Tracker!")
                break
            
            if not phone_input:
                continue
            
            print(f"\n🔍 Processing: {phone_input}")
            
            # Get phone info
            info, status = get_phone_info(phone_input)
            
            if info:
                print_info(info)
                
                # Additional validation
                from phonenumbers import parse, is_possible_number
                parsed = parse(phone_input if phone_input.startswith('+') else '+94' + phone_input.lstrip('0'), "LK")
                if is_possible_number(parsed):
                    print("✅ Number is possible and valid")
                else:
                    print("⚠️ Number format is unusual")
                    
            else:
                print(f"\n❌ {status}")
                print("💡 Tip: Use format +94701234567 or 0701234567")
                
        except KeyboardInterrupt:
            print("\n\n👋 Program terminated")
            break
        except Exception as e:
            print(f"\n⚠️ Error: {e}")

if __name__ == "__main__":
    main()
