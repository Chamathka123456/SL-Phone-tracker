#!/usr/bin/env python3
"""
Quick test for Sri Lankan Phone Tracker
"""

import phonenumbers
from phonenumbers import carrier, geocoder

def quick_test():
    print("🇱🇰 Quick Sri Lankan Phone Test")
    print("="*40)
    
    test_numbers = [
        "+94770851207",  # Dialog
        "0701234567",    # Mobitel
        "0771234567",    # Dialog
        "0812345678",    # Mobitel - Kandy
        "0112345678"     # Colombo landline
    ]
    
    for num_str in test_numbers:
        print(f"\n📞 Testing: {num_str}")
        
        # Format
        if num_str.startswith('0'):
            num_str = '+94' + num_str[1:]
        
        try:
            num = phonenumbers.parse(num_str, "LK")
            
            if phonenumbers.is_valid_number(num):
                print(f"  ✅ Valid Sri Lankan Number")
                print(f"  📡 Operator: {carrier.name_for_number(num, 'en')}")
                
                # Guess location from prefix
                prefix = num_str[3:5]
                locations = {
                    '70': 'Colombo/Urban Area',
                    '71': 'Colombo/Western Province',
                    '72': 'Colombo Metro',
                    '74': 'Colombo Suburbs',
                    '77': 'Dialog - Urban',
                    '81': 'Kandy Area'
                }
                print(f"  📍 Likely Location: {locations.get(prefix, 'Sri Lanka')}")
            else:
                print(f"  ❌ Invalid number")
        except:
            print(f"  ❌ Error processing")

if __name__ == "__main__":
    quick_test()
