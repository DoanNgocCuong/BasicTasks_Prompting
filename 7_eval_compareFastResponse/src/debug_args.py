#!/usr/bin/env python3
"""
Debug script để test argument parsing
"""
import sys
import argparse

def debug_parse_arguments():
    """
    Debug version of parse_arguments
    """
    print("🔍 DEBUG: Starting argument parsing debug...")
    print(f"🔍 DEBUG: Python version: {sys.version}")
    print(f"🔍 DEBUG: sys.argv = {sys.argv}")
    print(f"🔍 DEBUG: Number of arguments: {len(sys.argv)}")
    
    for i, arg in enumerate(sys.argv):
        print(f"🔍 DEBUG: argv[{i}] = '{arg}' (type: {type(arg).__name__}, len: {len(arg)})")
    
    parser = argparse.ArgumentParser(description='Debug Fast Response Evaluation Pipeline')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--ids', nargs='+', help='Conversation IDs (space separated)')
    group.add_argument('--id_file', type=str, help='File containing conversation IDs (one per line)')
    
    parser.add_argument('--token', type=str, default='{{token}}', 
                       help='API token (default: {{token}})')
    
    print("🔍 DEBUG: Parser created, attempting to parse...")
    
    try:
        args = parser.parse_args()
        print("✅ DEBUG: Parsing successful!")
        
        print(f"🔍 DEBUG: Parsed arguments:")
        print(f"🔍 DEBUG: args.ids = {getattr(args, 'ids', None)}")
        print(f"🔍 DEBUG: args.id_file = {getattr(args, 'id_file', None)}")
        print(f"🔍 DEBUG: args.token = '{args.token}'")
        print(f"🔍 DEBUG: len(args.token) = {len(args.token) if args.token else 0}")
        
        # Check if token looks like placeholder
        if args.token == '{{token}}':
            print("⚠️ DEBUG: Token is the placeholder '{{token}}'")
        elif '{{' in args.token or '}}' in args.token:
            print(f"⚠️ DEBUG: Token contains placeholder syntax: '{args.token}'")
        else:
            print(f"✅ DEBUG: Token appears to be a real value")
            
        return args
        
    except SystemExit as e:
        print(f"❌ DEBUG: SystemExit during parsing: {e}")
        print(f"🔍 DEBUG: Exit code: {e.code}")
        # Re-raise to show the error message
        raise
    except Exception as e:
        print(f"❌ DEBUG: Exception during parsing: {e}")
        print(f"🔍 DEBUG: Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    print("🧪 DEBUG SCRIPT FOR ARGUMENT PARSING")
    print("="*50)
    
    try:
        args = debug_parse_arguments()
        print("\n✅ DEBUG: Script completed successfully")
    except SystemExit as e:
        print(f"\n❌ DEBUG: Script exited with code: {e.code}")
        if e.code == 2:
            print("   This usually means there was an argument parsing error")
    except Exception as e:
        print(f"\n❌ DEBUG: Script failed with exception: {e}")