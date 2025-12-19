
import inspect
import sys
import os

# Import modules
# Assuming running from parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'freelanceros'))
from freelanceros.modules import business_math, text_data, system_files, media_web

MODULES = [business_math, text_data, system_files, media_web]

def load_registry():
    """Dynamically loads all functions from the modules."""
    registry = {}
    count = 0
    for mod in MODULES:
        for name, func in inspect.getmembers(mod, inspect.isfunction):
            if not name.startswith("_"): # Ignore internal
                registry[name] = func
                count += 1
    return registry, count

def main():
    tools, count = load_registry()
    
    print("\n" + "="*50)
    print(f" 🚀 FreelancerOS v1.0 | Loaded Tools: {count}")
    print("="*50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--count":
        print(f"Verified Tool Count: {count}")
        return

    print("Type a command (or 'list', 'exit'):")
    
    while True:
        try:
            cmd = input("FreelancerOS> ").strip()
            if cmd == "exit": break
            if cmd == "list":
                print(f"\nAvailable Tools ({count}):")
                for name in sorted(tools.keys()):
                    print(f" - {name}")
                continue
            
            if cmd in tools:
                func = tools[cmd]
                sig = inspect.signature(func)
                print(f"\n🔧 Executing: {cmd}{sig}")
                
                # Simple argument parser (Split by space, no type casting in MVP)
                args_str = input("   Enter arguments (space separated): ").strip()
                if args_str:
                    args = args_str.split()
                    # Try to convert to float/int if possible (naive)
                    clean_args = []
                    for a in args:
                        try:
                            if "." in a: clean_args.append(float(a))
                            else: clean_args.append(int(a))
                        except:
                            clean_args.append(a)
                    try:
                        res = func(*clean_args)
                        print(f"   ✅ Result: {res}")
                    except Exception as e:
                        print(f"   ❌ Execution Error: {e}")
                else:
                    try:
                        res = func()
                        print(f"   ✅ Result: {res}")
                    except Exception as e:
                        print(f"   ❌ Execution Error (Missing args?): {e}")

            else:
                print("⚠️ Unknown tool. Type 'list'.")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
